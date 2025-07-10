from django.db import models


class CustomUser(models.Model):
    username = models.CharField(max_length=150,null=False,blank=False, unique=True)
    password = models.CharField(max_length=500,null=False,blank=False)
    email = models.EmailField(null=False,blank=False)
    contact_number =  models.BigIntegerField(max_length=15,null=True, blank=True)
    role= models.CharField(max_length=50, null=False, blank=False)
    points=models.BigIntegerField(null=True, blank=True)



    def __str__(self):
        return self.username