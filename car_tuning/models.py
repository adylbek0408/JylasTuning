from django.db import models
from django.contrib.auth.models import User


class CarBrand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название марки")
    logo = models.FileField(upload_to='brands/logos/', verbose_name="Логотип марки")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Марка автомобиля"
        verbose_name_plural = "Марки автомобилей"


class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name='models', verbose_name="Бренд")
    name = models.CharField(max_length=100, verbose_name="Название модели")
    model_3d = models.FileField(upload_to='cars/3d_models/', verbose_name="3D модель")
    preview_image = models.FileField(upload_to='cars/preview/', blank=True, null=True, verbose_name="Превью")

    def __str__(self):
        return f"{self.brand.name} {self.name}"

    class Meta:
        verbose_name = "Модель автомобиля"
        verbose_name_plural = "Модели автомобилей"


class BaseCarPart(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название детали")
    model_3d = models.FileField(upload_to='parts/3d_models/', verbose_name="3D модель")
    image = models.FileField(upload_to='parts/images/', verbose_name="Изображение", blank=True, null=True)
    compatible_car_models = models.ManyToManyField(
        CarModel,
        related_name='%(class)s_compatible',
        verbose_name="Совместимые модели"
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        abstract = True
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Spoiler(BaseCarPart):
    class Meta:
        verbose_name = "Спойлер"
        verbose_name_plural = "Спойлеры"


class Discs(BaseCarPart):
    class Meta:
        verbose_name = "Диски"
        verbose_name_plural = "Диски"


class Restyling(BaseCarPart):
    class Meta:
        verbose_name = "Рестайлинг"
        verbose_name_plural = "Рестайлинг"


class Bumper(BaseCarPart):
    class Meta:
        verbose_name = "Передний бампер"
        verbose_name_plural = "Передние бамперы"


class RearBumper(BaseCarPart):
    class Meta:
        verbose_name = "Задний бампер"
        verbose_name_plural = "Задние бамперы"


class SideSkirt(BaseCarPart):
    class Meta:
        verbose_name = "Боковая юбка"
        verbose_name_plural = "Боковые юбки"


class Tinting(BaseCarPart):
    class Meta:
        verbose_name = "Тонировка"
        verbose_name_plural = "Тонировки"


class Color(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название цвета")
    hex_code = models.CharField(max_length=7, verbose_name="Код цвета (HEX)")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вариант цвета"
        verbose_name_plural = "Варианты цветов"
        ordering = ['order', 'name']


class UserCarCustomization(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название проекта", blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customizations',
        verbose_name="Пользователь"
    )
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        verbose_name="Модель автомобиля"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customizations',
        verbose_name="Цвет"
    )

    tinting = models.ForeignKey(
        Tinting,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Тонировка"
    )

    spoiler = models.ForeignKey(
        Spoiler,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Спойлер"
    )
    discs = models.ForeignKey(
        Discs,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Диски"
    )
    restyling = models.ForeignKey(
        Restyling,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Рестайлинг"
    )
    bumper = models.ForeignKey(
        Bumper,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Передний бампер"
    )
    rear_bumper = models.ForeignKey(
        RearBumper,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Задний бампер"
    )
    side_skirt = models.ForeignKey(
        SideSkirt,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Боковая юбка"
    )

    def __str__(self):
        return f"{self.user.username} - {self.car_model} ({self.name or 'Без названия'})"

    class Meta:
        verbose_name = "Кастомизация пользователя"
        verbose_name_plural = "Кастомизации пользователей"
