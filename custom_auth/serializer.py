from .models import AuthModel
from rest_framework import serializers


class AuthModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthModel
        fields = ['id', 'name', 'email', 'password', 'code']
    