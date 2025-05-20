from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from django.shortcuts import get_object_or_404

from .models import (
    CarBrand, CarModel, Spoiler, Discs, Restyling, Bumper,
    RearBumper, SideSkirt, Tinting, Color, UserCarCustomization
)
from .serializers import (
    CarBrandSerializer, CarModelSerializer, CarModelDetailSerializer,
    SpoilerSerializer, DiscsSerializer, RestylingSerializer, BumperSerializer,
    RearBumperSerializer, SideSkirtSerializer, TintingSerializer, ColorSerializer,
    UserCarCustomizationListSerializer, UserCarCustomizationDetailSerializer,
    UserCarCustomizationUpdateSerializer
)


class CarBrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CarBrand.objects.all().annotate(model_count=Count('models'))
    serializer_class = CarBrandSerializer


class CarModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CarModel.objects.select_related('brand').all()
    serializer_class = CarModelSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['detail'] = True
        return super().get_serializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        response_data = []

        if page is not None:
            for model in page:
                serializer = self.get_serializer(model)
                model_data = serializer.data
                compatible_parts = self.get_compatible_parts(model)
                for key, value in compatible_parts.items():
                    if key != 'colors':
                        model_data[key] = value
                response_data.append(model_data)
            return self.get_paginated_response(response_data)

        for model in queryset:
            serializer = self.get_serializer(model)
            model_data = serializer.data
            compatible_parts = self.get_compatible_parts(model)
            for key, value in compatible_parts.items():
                if key != 'colors':
                    model_data[key] = value
            response_data.append(model_data)

        return Response(response_data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        compatible_parts = self.get_compatible_parts(instance)
        serializer = self.get_serializer(instance)
        data = serializer.data
        for key, value in compatible_parts.items():
            if key != 'colors':
                data[key] = value
        return Response(data)

    def get_compatible_parts(self, car_model):
        mapping = {
            'spoilers': (Spoiler, SpoilerSerializer),
            'discs': (Discs, DiscsSerializer),
            'restylings': (Restyling, RestylingSerializer),
            'bumpers': (Bumper, BumperSerializer),
            'rear_bumpers': (RearBumper, RearBumperSerializer),
            'side_skirts': (SideSkirt, SideSkirtSerializer),
            'tintings': (Tinting, TintingSerializer),
        }
        data = {}
        for key, (model_cls, serializer_cls) in mapping.items():
            parts_qs = model_cls.objects.filter(
                compatible_car_models=car_model
            ).order_by('order')
            data[key] = serializer_cls(parts_qs, many=True).data

        colors = Color.objects.all().order_by('order')
        data['colors'] = ColorSerializer(colors, many=True).data
        return data

    @action(detail=True, methods=['get'])
    def compatible_parts(self, request, pk=None):
        car_model = self.get_object()
        data = self.get_compatible_parts(car_model)
        return Response(data)


class BasePartViewSet(viewsets.ReadOnlyModelViewSet):
    compatible_param = 'car_model_id'

    def get_queryset(self):
        qs = super().get_queryset()
        cm_id = self.request.query_params.get(self.compatible_param)
        if cm_id:
            qs = qs.filter(compatible_car_models__id=cm_id)
        return qs


class SpoilerViewSet(BasePartViewSet):
    queryset = Spoiler.objects.all()
    serializer_class = SpoilerSerializer


class DiscsViewSet(BasePartViewSet):
    queryset = Discs.objects.all()
    serializer_class = DiscsSerializer


class RestylingViewSet(BasePartViewSet):
    queryset = Restyling.objects.all()
    serializer_class = RestylingSerializer


class BumperViewSet(BasePartViewSet):
    queryset = Bumper.objects.all()
    serializer_class = BumperSerializer


class RearBumperViewSet(BasePartViewSet):
    queryset = RearBumper.objects.all()
    serializer_class = RearBumperSerializer


class SideSkirtViewSet(BasePartViewSet):
    queryset = SideSkirt.objects.all()
    serializer_class = SideSkirtSerializer


class TintingViewSet(BasePartViewSet):
    queryset = Tinting.objects.all()
    serializer_class = TintingSerializer


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Color.objects.all().order_by('order')
    serializer_class = ColorSerializer


class UserCarCustomizationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            UserCarCustomization.objects
            .filter(user=self.request.user)
            .select_related(
                'car_model', 'car_model__brand',
                'color', 'tinting', 'spoiler', 'discs',
                'restyling', 'bumper', 'rear_bumper', 'side_skirt'
            )
            .order_by('-updated_at')
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return UserCarCustomizationListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return UserCarCustomizationUpdateSerializer
        return UserCarCustomizationDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'])
    def update_part(self, request, pk=None):
        customization = self.get_object()
        part_type = request.data.get('part_type')
        part_id = request.data.get('part_id')

        if not part_type or (part_id is None and part_id != ''):
            return Response(
                {'error': 'Укажите тип детали и ID детали'},
                status=status.HTTP_400_BAD_REQUEST
            )

        mapping = {
            'spoiler': Spoiler, 'discs': Discs,
            'restyling': Restyling, 'bumper': Bumper,
            'rear_bumper': RearBumper, 'side_skirt': SideSkirt,
            'tinting': Tinting, 'color': Color,
        }
        cls = mapping.get(part_type)
        if cls is None:
            return Response(
                {'error': f'Неизвестный тип детали: {part_type}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        lookup = {'id': part_id}
        if cls is not Color:
            lookup['compatible_car_models'] = customization.car_model

        new_part = get_object_or_404(cls, **lookup) if part_id else None
        setattr(customization, part_type, new_part)
        customization.save()

        return Response(UserCarCustomizationDetailSerializer(customization).data)
