# Generated by Django 3.0.7 on 2020-06-13 09:48

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
            name='request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField()),
                ('sector', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='can',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.request')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User')),
            ],
        ),
        migrations.CreateModel(
            name='belongs_to',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ngo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.request')),
                ('request_to', models.CharField(max_length=20)),
            ],
        ),
    ]
