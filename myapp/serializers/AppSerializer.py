from rest_framework import serializers
from myapp.models.App import App

class AppSerializer(serializers.ModelSerializer):
    username=serializers.ReadOnlyField(source='user.username')

    class Meta:
        model=App
        fields=[
            'id',
            'name',
            'publisher',
            'app_logo',
            'points',
            'username',
            'added_on'
            ]