# Generated by Django 3.1.7 on 2021-03-17 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario', '0015_delete_formularioseguridad'),
    ]

    operations = [
        migrations.AddField(
            model_name='formularioomil',
            name='nombre_formulario',
            field=models.CharField(default='Formulario OMIL', editable=False, max_length=20),
        ),
    ]
