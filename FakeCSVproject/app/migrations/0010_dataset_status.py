# Generated by Django 3.2.4 on 2021-06-18 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210618_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='status',
            field=models.CharField(choices=[('Processing', 'Processing'), ('Ready', 'Ready')], default='Processing', max_length=20),
        ),
    ]