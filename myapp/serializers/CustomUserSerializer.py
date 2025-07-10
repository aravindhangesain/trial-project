
from rest_framework import serializers
from myapp.models.CustomUser import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = CustomUser
        fields = ['id', 
                  'username', 
                  'email', 
                  'password', 
                  'contact_number',
                  'role',
                  'points'
                ]