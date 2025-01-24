from django.db import models

from authentication.models import User

# Create your models here.
class Uploads(models.Model):
    file = models.FileField(upload_to='uploads/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class tests(models.Model):
    file = models.ForeignKey(Uploads, on_delete= models.CASCADE)
    description = models.CharField(max_length= 50)
    result = models.IntegerField()
    range = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
