# Generated by Django 4.1.3 on 2023-03-18 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Prakruti_App', '0020_prakruti_quetions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint_Quetions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('que', models.TextField(default='')),
                ('choice1', models.TextField(default='')),
                ('choice2', models.TextField(default='')),
                ('prakruti', models.TextField(default='')),
            ],
        ),
    ]
