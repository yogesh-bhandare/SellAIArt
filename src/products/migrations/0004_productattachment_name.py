# Generated by Django 5.1.1 on 2024-09-30 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productattachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattachment',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
