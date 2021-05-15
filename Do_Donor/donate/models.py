from django.db import models

# Create your models here.
class Destination(models.Model):
    title = models.CharField(max_length=200)
    des = models.TextField()
    img = models.ImageField(upload_to='pics')
    b_text = models.CharField(max_length=100)

    def __str__(self):
        return self.title
