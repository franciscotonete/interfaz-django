# Generated by Django 3.1.7 on 2021-04-20 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formulario', '0020_auto_20210420_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seguridad',
            name='autor',
        ),
        migrations.DeleteModel(
            name='Farmacia',
        ),
        migrations.DeleteModel(
            name='Seguridad',
        ),
    ]
