# Generated by Django 4.1.4 on 2023-02-16 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Prakruti_App', '0017_merge_20230203_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]