# Generated by Django 2.0 on 2020-01-17 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_mailbag_local'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailbag',
            name='alias',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
