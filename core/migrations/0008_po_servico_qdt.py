# Generated by Django 2.0 on 2020-01-17 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200117_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='po',
            name='servico_qdt',
            field=models.IntegerField(default=0, verbose_name='Quantidade'),
        ),
    ]