# Generated by Django 3.0.7 on 2020-06-25 05:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ngodata',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('r_no', models.CharField(max_length=10)),
                ('ngo_name', models.CharField(max_length=100)),
                ('img', models.ImageField(upload_to='pics')),
                ('zip', models.IntegerField()),
                ('mobile', models.CharField(max_length=20)),
                ('sector', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('status', models.CharField(default='NV', max_length=100)),
            ],
        ),
    ]
