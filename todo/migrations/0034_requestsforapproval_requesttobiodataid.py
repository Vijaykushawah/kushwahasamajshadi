# Generated by Django 3.1.1 on 2020-10-05 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0033_requestsforapproval_requesttousername'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestsforapproval',
            name='requesttobiodataid',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
