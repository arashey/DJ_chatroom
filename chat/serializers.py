from rest_framework import serializers
from .models import Room, Message
from django.contrib.auth.models import User

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id']


class Messageserializer(serializers.ModelSerializer):
    sender = Userserializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'content', 'timestamp']
        read_only_fields = ['sender']


class Roomserializer(serializers.ModelSerializer):
    created_by = Userserializer(read_only=True)
    message = Messageserializer(many=True, read_only=True)
    
    class Meta:
        model = Room
        fields = ['id', 'name', 'created_at', 'created_by', 'message']
        read_only_fields = ['created_by']



