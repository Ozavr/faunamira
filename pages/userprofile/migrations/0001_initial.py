# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 12:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Men'), ('W', 'Woman')], max_length=1, null=True, verbose_name='Gender')),
                ('phone', models.CharField(blank=True, max_length=30, null=True, verbose_name='Phone')),
                ('info', models.TextField(blank=True, null=True, verbose_name='About me')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Birthday')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='profile/avatar', verbose_name='Avatar')),
                ('vk', models.URLField(blank=True, max_length=100, null=True, verbose_name='Vkontakte')),
                ('ok', models.URLField(blank=True, max_length=100, null=True, verbose_name='Odnoklassniki')),
                ('fb', models.URLField(blank=True, max_length=100, null=True, verbose_name='Facebook')),
                ('insta', models.URLField(blank=True, max_length=100, null=True, verbose_name='Instagram')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='ProfileImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='profile/images', verbose_name='Photo')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date added')),
                ('description', models.CharField(blank=True, max_length=250, null=True, verbose_name='Description')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Profile image',
                'verbose_name_plural': 'Profile images ',
                'ordering': ['-date'],
            },
        ),
    ]
