from django.db import models

from account.models import User

# Create your models here.
class ngodata(models.Model):
    user = models.OneToOneField(User, to_field='id', primary_key=True, on_delete=models.CASCADE)
    r_no = models.CharField(max_length=10)
    ngo_name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    zip = models.IntegerField()
    mobile = models.CharField(max_length=20)
    sector = models.CharField(max_length=100)
    desc = models.TextField()
    status = models.CharField(max_length=100, default='NV', editable=True)

    def __str__(self):
        return self.ngo_name