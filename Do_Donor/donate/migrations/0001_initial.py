# Generated by Django 3.0.7 on 2020-06-24 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('des', models.TextField()),
                ('img', models.ImageField(upload_to='pics')),
                ('b_text', models.CharField(max_length=100)),
            ],
        ),
    ]
