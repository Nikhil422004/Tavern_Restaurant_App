# Generated by Django 5.0.6 on 2024-07-02 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='./profile_pics/default.jpg', upload_to='profile_pics'),
        ),
    ]
