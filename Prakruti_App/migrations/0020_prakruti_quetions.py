# Generated by Django 4.1.3 on 2023-02-19 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Prakruti_App', '0019_delete_prakruti_quetions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prakruti_Quetions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('que', models.TextField(default='')),
                ('choice1', models.TextField(default='')),
                ('choice2', models.TextField(default='')),
                ('choice3', models.TextField(default='')),
                ('choice4', models.TextField(default='')),
            ],
        ),
    ]