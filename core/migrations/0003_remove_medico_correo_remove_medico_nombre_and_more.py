# Generated by Django 4.2.6 on 2023-12-02 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_reserva_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medico',
            name='correo',
        ),
        migrations.RemoveField(
            model_name='medico',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='correo',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='secretaria',
            name='correo',
        ),
        migrations.RemoveField(
            model_name='secretaria',
            name='nombre',
        ),
    ]
