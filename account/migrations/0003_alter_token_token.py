# Generated by Django 4.2.5 on 2023-09-30 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_token_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
