from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from ngo.models import ngodata
from account.models import User
# Create your models here.

class requests(models.Model):

    location = models.TextField()
    sector = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateField()
    verified = models.BooleanField(default=False)
# Create your models here.


class can(models.Model):
    class Meta:
         managed = False
    request = models.ForeignKey(requests, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class belongs_to(models.Model):
    class Meta:
         managed = False
    request = models.ForeignKey(requests, on_delete=models.CASCADE)
    ngo = models.ForeignKey(User, on_delete=models.CASCADE)
    request_to= models.CharField(max_length=20)





