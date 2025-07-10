from django.db import models
from django.utils import timezone

class App(models.Model):
    name=models.CharField(max_length=120,null=False,blank=False,unique=True)
    publisher=models.CharField(max_length=120,null=False,blank=False)
    app_logo=models.ImageField(upload_to='app_logos/',null=True,blank=True)
    points=models.IntegerField(null=False,blank=False)
    user=models.ForeignKey('CustomUser',on_delete=models.CASCADE,null=True,blank=True)
    added_on = models.DateTimeField(default=timezone.now)
