# Generated by Django 4.0.4 on 2022-05-30 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phone_attrib', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]