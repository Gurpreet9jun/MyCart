# Generated by Django 2.2 on 2019-12-20 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpost_image1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image1',
            field=models.ImageField(default='', upload_to='blog/images'),
        ),
    ]
