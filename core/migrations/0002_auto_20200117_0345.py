# Generated by Django 2.0 on 2020-01-17 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailbag',
            name='entrega',
            field=models.IntegerField(choices=[(1, 'manhã 08:00'), (2, 'tarde 11:00'), (3, 'manhã 14:00'), (4, 'manhã 16:00')], default=1),
        ),
    ]
