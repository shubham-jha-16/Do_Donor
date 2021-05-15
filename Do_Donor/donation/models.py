from django.db import models
from django.contrib.auth.models import User
from ngo.models import ngodata
from account.models import User

# Create your models here.
class donation_data(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    ngo = models.ForeignKey(ngodata, on_delete=models.CASCADE)
    address = models.TextField()
    sector = models.TextField()
    category = models.CharField(max_length=300)
    quantity = models.IntegerField(default='0', editable=True)
    mode = models.CharField(max_length=100)
    date = models.DateField()
    pickup_time = models.CharField(max_length=100, default='none', editable=True)
    amount = models.CharField(max_length=100,default='0', editable=True)
