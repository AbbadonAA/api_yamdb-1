# Generated by Django 3.0 on 2022-03-03 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220303_0341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
