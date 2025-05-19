from rest_framework import serializers
from django.db.models import Count
from .models import (
    CarBrand, CarModel, Spoiler, Discs, Restyling, Bumper,
    RearBumper, SideSkirt, Tinting, Color, UserCarCustomization
)


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']


class CarBrandSerializer(serializers.ModelSerializer):
    model_count = serializers.SerializerMethodField()

    class Meta:
        model = CarBrand
        fields = ['id', 'name', 'logo', 'model_count']

    def get_model_count(self, obj):
        return obj.models.count()


class CarModelSerializer(serializers.ModelSerializer):
    """
    Универсальный сериализатор для моделей автомобилей.
    При detail=True включает полный объект brand, иначе только brand_name.
    """
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    brand = CarBrandSerializer(read_only=True)
    coming_soon = serializers.SerializerMethodField()

    class Meta:
        model = CarModel
        fields = ['id', 'name', 'brand', 'brand_name', 'model_3d', 'preview_image', 'coming_soon']

    def __init__(self, *args, **kwargs):
        # Извлекаем параметр detail, по умолчанию False
        self.detail = kwargs.pop('detail', False)
        super().__init__(*args, **kwargs)

        # Если не detail-представление, убираем лишние поля
        if not self.detail:
            self.fields.pop('brand')
            self.fields.pop('model_3d')
        else:
            # Если detail-представление, убираем brand_name (т.к. есть полный brand)
            self.fields.pop('brand_name')

    def get_coming_soon(self, obj):
        flag = obj.coming_soon_flag.first()
        return flag.coming_soon if flag else False


class BaseCarPartSerializer(serializers.ModelSerializer):
    coming_soon = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'name', 'model_3d', 'image', 'coming_soon']

    def get_coming_soon(self, obj):
        flag = obj.coming_soon_flag.first()
        return flag.coming_soon if flag else False


class SpoilerSerializer(BaseCarPartSerializer):
    class Meta(BaseCarPartSerializer.Meta):
        model = Spoiler


class DiscsSerializer(BaseCarPartSerializer):
    class Meta(BaseCarPartSerializer.Meta):
        model = Discs


class RestylingSerializer(BaseCarPartSerializer):
    class Meta(BaseCarPartSerializer.Meta):
        model = Restyling


class BumperSerializer(BaseCarPartSerializer):
    class Meta(BaseCarPartSerializer.Meta):
        model = Bumper


class RearBumperSerializer(BaseCarPartSerializer):
    class Meta(BaseCarPartSerializer.Meta):
        model = RearBumper


class SideSkirtSerializer(BaseCarPartSerializer):
    class Meta(BaseCarPartSerializer.Meta):
        model = SideSkirt


class TintingSerializer(BaseCarPartSerializer):
    class Meta(BaseCarPartSerializer.Meta):
        model = Tinting


class UserCarCustomizationListSerializer(serializers.ModelSerializer):
    car_model_name = serializers.CharField(source='car_model.__str__', read_only=True)

    class Meta:
        model = UserCarCustomization
        fields = ['id', 'name', 'car_model_name', 'created_at', 'updated_at']


class UserCarCustomizationDetailSerializer(serializers.ModelSerializer):
    car_model = CarModelSerializer(read_only=True, detail=True)
    color = ColorSerializer(read_only=True)
    tinting = TintingSerializer(read_only=True)
    spoiler = SpoilerSerializer(read_only=True)
    discs = DiscsSerializer(read_only=True)
    restyling = RestylingSerializer(read_only=True)
    bumper = BumperSerializer(read_only=True)
    rear_bumper = RearBumperSerializer(read_only=True)
    side_skirt = SideSkirtSerializer(read_only=True)

    class Meta:
        model = UserCarCustomization
        fields = [
            'id', 'name', 'user', 'car_model', 'created_at', 'updated_at',
            'color', 'tinting', 'spoiler', 'discs', 'restyling',
            'bumper', 'rear_bumper', 'side_skirt'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


class UserCarCustomizationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCarCustomization
        fields = [
            'name', 'car_model', 'color', 'tinting', 'spoiler', 'discs',
            'restyling', 'bumper', 'rear_bumper', 'side_skirt'
        ]

    def validate(self, data):
        car_model = data.get('car_model', self.instance.car_model if self.instance else None)

        for field_name in ['spoiler', 'discs', 'restyling', 'bumper', 'rear_bumper', 'side_skirt', 'tinting']:
            part = data.get(field_name)
            if part and not part.compatible_car_models.filter(id=car_model.id).exists():
                raise serializers.ValidationError({
                    field_name: f"Эта деталь несовместима с выбранной моделью автомобиля ({car_model})"
                })

        return data


class CompatiblePartsSerializer(serializers.Serializer):
    spoilers = SpoilerSerializer(many=True, read_only=True)
    discs = DiscsSerializer(many=True, read_only=True)
    restylings = RestylingSerializer(many=True, read_only=True)
    bumpers = BumperSerializer(many=True, read_only=True)
    rear_bumpers = RearBumperSerializer(many=True, read_only=True)
    side_skirts = SideSkirtSerializer(many=True, read_only=True)
    tintings = TintingSerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
