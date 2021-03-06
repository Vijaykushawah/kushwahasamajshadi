# Generated by Django 3.1.1 on 2020-10-03 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0021_auto_20201003_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biodataprivacy',
            name='address_detail_visibility',
            field=models.CharField(choices=[('Visible_To_All', 'Visible To All'), ('Visible_To_ME', 'Visible To Me'), ('Hidden', 'Hidden'), ('Not_Specified', 'Not Specified')], default='Visible_To_All', max_length=20),
        ),
        migrations.AlterField(
            model_name='biodataprivacy',
            name='education_detail_visibility',
            field=models.CharField(choices=[('Visible_To_All', 'Visible To All'), ('Visible_To_ME', 'Visible To Me'), ('Hidden', 'Hidden'), ('Not_Specified', 'Not Specified')], default='Visible_To_All', max_length=20),
        ),
    ]
