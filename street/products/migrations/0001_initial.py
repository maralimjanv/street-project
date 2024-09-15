# Generated by Django 4.2.11 on 2024-09-02 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name_uz', models.CharField(max_length=20)),
                ('name_ru', models.CharField(max_length=20)),
                ('name_eng', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('chat_id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('lang', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20, null=True)),
                ('contact', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('caption', models.TextField()),
                ('photo', models.TextField()),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
        ),
        migrations.CreateModel(
            name='Branches',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('lat', models.CharField(max_length=30)),
                ('lon', models.CharField(max_length=30)),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.city')),
            ],
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('count', models.SmallIntegerField(default=1)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.items')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.user')),
            ],
        ),
    ]