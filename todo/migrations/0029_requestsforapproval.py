# Generated by Django 3.1.1 on 2020-10-05 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0028_auto_20201004_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestsForApproval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestfromusername', models.CharField(blank=True, max_length=200)),
                ('contact_view_request', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('Not_Specified', 'Not Specified')], default='Not_Specified', max_length=20)),
                ('connect_request', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('Not_Specified', 'Not Specified')], default='Not_Specified', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
