from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch, Count
from django.shortcuts import get_object_or_404

from .models import (
    CarBrand, CarModel, Spoiler, Discs, Restyling, Bumper,
    RearBumper, SideSkirt, Tinting, Color, UserCarCustomization
)
from .serializers import (
    CarBrandSerializer, CarModelListSerializer, CarModelDetailSerializer,
    SpoilerSerializer, DiscsSerializer, RestylingSerializer, BumperSerializer,
    RearBumperSerializer, SideSkirtSerializer, TintingSerializer, ColorSerializer,
    UserCarCustomizationListSerializer, UserCarCustomizationDetailSerializer,
    UserCarCustomizationUpdateSerializer, CompatiblePartsSerializer
)


class CarBrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CarBrand.objects.all().annotate(model_count=Count('models'))
    serializer_class = CarBrandSerializer


class CarModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CarModel.objects.all().select_related('brand')

    def get_serializer_class(self):
        if self.action == 'list':
            return CarModelListSerializer
        return CarModelDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        brand_id = self.request.query_params.get('brand_id')
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        return queryset

    @action(detail=True, methods=['get'])
    def compatible_parts(self, request, pk=None):
        car_model = self.get_object()

        spoilers = Spoiler.objects.filter(compatible_car_models=car_model).order_by('order')
        discs = Discs.objects.filter(compatible_car_models=car_model).order_by('order')
        restylings = Restyling.objects.filter(compatible_car_models=car_model).order_by('order')
        bumpers = Bumper.objects.filter(compatible_car_models=car_model).order_by('order')
        rear_bumpers = RearBumper.objects.filter(compatible_car_models=car_model).order_by('order')
        side_skirts = SideSkirt.objects.filter(compatible_car_models=car_model).order_by('order')
        tintings = Tinting.objects.filter(compatible_car_models=car_model).order_by('order')
        colors = Color.objects.all().order_by('order')

        data = {
            'spoilers': SpoilerSerializer(spoilers, many=True).data,
            'discs': DiscsSerializer(discs, many=True).data,
            'restylings': RestylingSerializer(restylings, many=True).data,
            'bumpers': BumperSerializer(bumpers, many=True).data,
            'rear_bumpers': RearBumperSerializer(rear_bumpers, many=True).data,
            'side_skirts': SideSkirtSerializer(side_skirts, many=True).data,
            'tintings': TintingSerializer(tintings, many=True).data,
            'colors': ColorSerializer(colors, many=True).data,
        }

        return Response(data)


class SpoilerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Spoiler.objects.all()
    serializer_class = SpoilerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        car_model_id = self.request.query_params.get('car_model_id')
        if car_model_id:
            queryset = queryset.filter(compatible_car_models__id=car_model_id)
        return queryset


class DiscsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Discs.objects.all()
    serializer_class = DiscsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        car_model_id = self.request.query_params.get('car_model_id')
        if car_model_id:
            queryset = queryset.filter(compatible_car_models__id=car_model_id)
        return queryset


class RestylingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restyling.objects.all()
    serializer_class = RestylingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        car_model_id = self.request.query_params.get('car_model_id')
        if car_model_id:
            queryset = queryset.filter(compatible_car_models__id=car_model_id)
        return queryset


class BumperViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bumper.objects.all()
    serializer_class = BumperSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        car_model_id = self.request.query_params.get('car_model_id')
        if car_model_id:
            queryset = queryset.filter(compatible_car_models__id=car_model_id)
        return queryset


class RearBumperViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RearBumper.objects.all()
    serializer_class = RearBumperSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        car_model_id = self.request.query_params.get('car_model_id')
        if car_model_id:
            queryset = queryset.filter(compatible_car_models__id=car_model_id)
        return queryset


class SideSkirtViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SideSkirt.objects.all()
    serializer_class = SideSkirtSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        car_model_id = self.request.query_params.get('car_model_id')
        if car_model_id:
            queryset = queryset.filter(compatible_car_models__id=car_model_id)
        return queryset


class TintingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tinting.objects.all()
    serializer_class = TintingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        car_model_id = self.request.query_params.get('car_model_id')
        if car_model_id:
            queryset = queryset.filter(compatible_car_models__id=car_model_id)
        return queryset


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Color.objects.all().order_by('order')
    serializer_class = ColorSerializer


class UserCarCustomizationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserCarCustomization.objects.filter(user=self.request.user).select_related(
            'car_model', 'car_model__brand', 'color', 'tinting',
            'spoiler', 'discs', 'restyling', 'bumper', 'rear_bumper', 'side_skirt'
        ).order_by('-updated_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return UserCarCustomizationListSerializer
        elif self.action in ['update', 'partial_update', 'create']:
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
                {'error': 'Укажите тип детали (part_type) и ID детали (part_id)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if part_id:
            try:
                part_class = {
                    'spoiler': Spoiler,
                    'discs': Discs,
                    'restyling': Restyling,
                    'bumper': Bumper,
                    'rear_bumper': RearBumper,
                    'side_skirt': SideSkirt,
                    'tinting': Tinting,
                    'color': Color
                }.get(part_type)

                if part_class:
                    if part_class == Color:
                        part = get_object_or_404(part_class, id=part_id)
                    else:
                        part = get_object_or_404(
                            part_class,
                            id=part_id,
                            compatible_car_models=customization.car_model
                        )

                    setattr(customization, part_type, part)
                else:
                    return Response(
                        {'error': f'Неизвестный тип детали: {part_type}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Exception as e:
                return Response(
                    {'error': f'Деталь не найдена или несовместима: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            setattr(customization, part_type, None)

        customization.save()
        return Response(
            UserCarCustomizationDetailSerializer(customization).data
        )
