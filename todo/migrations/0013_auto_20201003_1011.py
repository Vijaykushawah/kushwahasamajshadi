# Generated by Django 3.1.1 on 2020-10-03 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0012_auto_20201003_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mybiodata',
            name='complexion',
            field=models.CharField(choices=[('ff', 'Fair'), ('mm', 'Milky Fair'), ('vf', 'Very Fair'), ('br', 'Brown'), ('dd', 'Dark'), ('nn', 'Normal'), ('ns', 'Not Specified')], default='ff', max_length=2),
        ),
    ]
