from django.db import models
from django.utils import timezone


class UserApps(models.Model):
    user= models.ForeignKey('CustomUser',on_delete=models.CASCADE,null=False,blank=False)
    app= models.ForeignKey('App',on_delete=models.CASCADE,null=False,blank=False)
    added_on = models.DateTimeField(default=timezone.now)
    screenshots=models.ImageField(upload_to='screenshots/',null=False,blank=False)