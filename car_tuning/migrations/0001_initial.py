# Generated by Django 5.2 on 2025-04-10 12:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название марки')),
                ('logo', models.FileField(upload_to='brands/logos/', verbose_name='Логотип марки')),
            ],
            options={
                'verbose_name': 'Марка автомобиля',
                'verbose_name_plural': 'Марки автомобилей',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название цвета')),
                ('hex_code', models.CharField(max_length=7, verbose_name='Код цвета (HEX)')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок отображения')),
            ],
            options={
                'verbose_name': 'Вариант цвета',
                'verbose_name_plural': 'Варианты цветов',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название модели')),
                ('model_3d', models.FileField(upload_to='cars/3d_models/', verbose_name='3D модель')),
                ('preview_image', models.FileField(blank=True, null=True, upload_to='cars/preview/', verbose_name='Превью')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='car_tuning.carbrand', verbose_name='Бренд')),
            ],
            options={
                'verbose_name': 'Модель автомобиля',
                'verbose_name_plural': 'Модели автомобилей',
            },
        ),
        migrations.CreateModel(
            name='Bumper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название детали')),
                ('model_3d', models.FileField(upload_to='parts/3d_models/', verbose_name='3D модель')),
                ('image', models.FileField(blank=True, null=True, upload_to='parts/images/', verbose_name='Изображение')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок отображения')),
                ('compatible_car_models', models.ManyToManyField(related_name='%(class)s_compatible', to='car_tuning.carmodel', verbose_name='Совместимые модели')),
            ],
            options={
                'verbose_name': 'Передний бампер',
                'verbose_name_plural': 'Передние бамперы',
            },
        ),
        migrations.CreateModel(
            name='Discs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название детали')),
                ('model_3d', models.FileField(upload_to='parts/3d_models/', verbose_name='3D модель')),
                ('image', models.FileField(blank=True, null=True, upload_to='parts/images/', verbose_name='Изображение')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок отображения')),
                ('compatible_car_models', models.ManyToManyField(related_name='%(class)s_compatible', to='car_tuning.carmodel', verbose_name='Совместимые модели')),
            ],
            options={
                'verbose_name': 'Диски',
                'verbose_name_plural': 'Диски',
            },
        ),
        migrations.CreateModel(
            name='RearBumper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название детали')),
                ('model_3d', models.FileField(upload_to='parts/3d_models/', verbose_name='3D модель')),
                ('image', models.FileField(blank=True, null=True, upload_to='parts/images/', verbose_name='Изображение')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок отображения')),
                ('compatible_car_models', models.ManyToManyField(related_name='%(class)s_compatible', to='car_tuning.carmodel', verbose_name='Совместимые модели')),
            ],
            options={
                'verbose_name': 'Задний бампер',
                'verbose_name_plural': 'Задние бамперы',
            },
        ),
        migrations.CreateModel(
            name='Restyling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название детали')),
                ('model_3d', models.FileField(upload_to='parts/3d_models/', verbose_name='3D модель')),
                ('image', models.FileField(blank=True, null=True, upload_to='parts/images/', verbose_name='Изображение')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок отображения')),
                ('compatible_car_models', models.ManyToManyField(related_name='%(class)s_compatible', to='car_tuning.carmodel', verbose_name='Совместимые модели')),
            ],
            options={
                'verbose_name': 'Рестайлинг',
                'verbose_name_plural': 'Рестайлинг',
            },
        ),
        migrations.CreateModel(
            name='SideSkirt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название детали')),
                ('model_3d', models.FileField(upload_to='parts/3d_models/', verbose_name='3D модель')),
                ('image', models.FileField(blank=True, null=True, upload_to='parts/images/', verbose_name='Изображение')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок отображения')),
                ('compatible_car_models', models.ManyToManyField(related_name='%(class)s_compatible', to='car_tuning.carmodel', verbose_name='Совместимые модели')),
            ],
            options={
                'verbose_name': 'Боковая юбка',
                'verbose_name_plural': 'Боковые юбки',
            },
        ),
        migrations.CreateModel(
            name='Spoiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название детали')),
                ('model_3d', models.FileField(upload_to='parts/3d_models/', verbose_name='3D модель')),
                ('image', models.FileField(blank=True, null=True, upload_to='parts/images/', verbose_name='Изображение')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок отображения')),
                ('compatible_car_models', models.ManyToManyField(related_name='%(class)s_compatible', to='car_tuning.carmodel', verbose_name='Совместимые модели')),
            ],
            options={
                'verbose_name': 'Спойлер',
                'verbose_name_plural': 'Спойлеры',
            },
        ),
        migrations.CreateModel(
            name='Tinting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название детали')),
                ('model_3d', models.FileField(upload_to='parts/3d_models/', verbose_name='3D модель')),
                ('image', models.FileField(blank=True, null=True, upload_to='parts/images/', verbose_name='Изображение')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок отображения')),
                ('compatible_car_models', models.ManyToManyField(related_name='%(class)s_compatible', to='car_tuning.carmodel', verbose_name='Совместимые модели')),
            ],
            options={
                'verbose_name': 'Тонировка',
                'verbose_name_plural': 'Тонировки',
            },
        ),
        migrations.CreateModel(
            name='UserCarCustomization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='Название проекта')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('bumper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='car_tuning.bumper', verbose_name='Передний бампер')),
                ('car_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_tuning.carmodel', verbose_name='Модель автомобиля')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customizations', to='car_tuning.color', verbose_name='Цвет')),
                ('discs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='car_tuning.discs', verbose_name='Диски')),
                ('rear_bumper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='car_tuning.rearbumper', verbose_name='Задний бампер')),
                ('restyling', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='car_tuning.restyling', verbose_name='Рестайлинг')),
                ('side_skirt', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='car_tuning.sideskirt', verbose_name='Боковая юбка')),
                ('spoiler', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='car_tuning.spoiler', verbose_name='Спойлер')),
                ('tinting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='car_tuning.tinting', verbose_name='Тонировка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customizations', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Кастомизация пользователя',
                'verbose_name_plural': 'Кастомизации пользователей',
            },
        ),
    ]
