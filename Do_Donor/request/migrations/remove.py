
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),

    ]

    operations = [
        migrations.RemoveField(
            model_name='can',
            name='id'
        )

        ,
        migrations.RemoveField(
            model_name='belongs_to',
            name='id'
        )
    ]


