from rest_framework import serializers
from django.contrib.auth.models import User

class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')