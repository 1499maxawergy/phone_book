# serualizers.py

from rest_framework import serializers

from .models import PhoneBook

class PhoneBookSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=60)
    phone = serializers.CharField(max_length=60)
    email = serializers.CharField(max_length=60)
    title = serializers.CharField(max_length=60)


    class Meta:
        model = PhoneBook
        fields = ('id', 'name', 'phone', 'email', 'title')