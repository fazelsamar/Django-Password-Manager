# Generated by Django 4.2.5 on 2023-09-30 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_token_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expired',
            field=models.DateTimeField(default='2000-01-01'),
        ),
    ]
