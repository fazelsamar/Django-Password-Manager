# Generated by Django 4.2.5 on 2023-09-30 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_token_otp_token_otp_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expired',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]