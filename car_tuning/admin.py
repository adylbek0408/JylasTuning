from django.contrib import admin
from django.utils.html import format_html
from .models import (
    CarBrand, CarModel, Spoiler, Discs, Restyling, Bumper,
    RearBumper, SideSkirt, Tinting, Color, UserCarCustomization
)


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_logo', 'model_count')
    search_fields = ('name',)

    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo.url)
        return "Нет логотипа"

    display_logo.short_description = "Логотип"

    def model_count(self, obj):
        return obj.models.count()

    model_count.short_description = "Количество моделей"


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'brand', 'display_preview')
    list_filter = ('brand',)
    search_fields = ('name', 'brand__name')

    def display_preview(self, obj):
        if obj.preview_image:
            return format_html('<img src="{}" width="100" height="60" />', obj.preview_image.url)
        return "Нет превью"

    display_preview.short_description = "Превью"


class BaseCarPartAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_image', 'order')
    list_filter = ('compatible_car_models', 'compatible_car_models__brand')
    search_fields = ('name',)
    filter_horizontal = ('compatible_car_models',)

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" />', obj.image.url)
        return "Нет изображения"

    display_image.short_description = "Изображение"


@admin.register(Spoiler)
class SpoilerAdmin(BaseCarPartAdmin):
    pass


@admin.register(Discs)
class DiscsAdmin(BaseCarPartAdmin):
    pass


@admin.register(Restyling)
class RestylingAdmin(BaseCarPartAdmin):
    pass


@admin.register(Bumper)
class BumperAdmin(BaseCarPartAdmin):
    pass


@admin.register(RearBumper)
class RearBumperAdmin(BaseCarPartAdmin):
    pass


@admin.register(SideSkirt)
class SideSkirtAdmin(BaseCarPartAdmin):
    pass


@admin.register(Tinting)
class TintingAdmin(BaseCarPartAdmin):
    pass


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_color', 'hex_code', 'order')
    search_fields = ('name', 'hex_code')

    def display_color(self, obj):
        return format_html(
            '<div style="width:30px; height:30px; background-color:{0}; border:1px solid #ccc"></div>',
            obj.hex_code
        )

    display_color.short_description = "Цвет"


@admin.register(UserCarCustomization)
class UserCarCustomizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'car_model', 'created_at', 'updated_at')
    list_filter = ('user', 'car_model__brand', 'car_model')
    search_fields = ('name', 'user__username', 'car_model__name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'user', 'car_model', 'created_at', 'updated_at')
        }),
        ('Кастомизация', {
            'fields': (
                'color', 'tinting', 'spoiler', 'discs', 'restyling',
                'bumper', 'rear_bumper', 'side_skirt'
            )
        }),
    )
