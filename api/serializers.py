from .models import Task
from django.contrib.auth.models import User
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    # serializer for the task model, probably will have override some of the
    # methods for the user to be able to update, delete and so on
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'user']
        read_only_fields = ['user'] # had to put user as read only, since the user will be set in the view
    
    def create(self, validated_data):
        task = Task.objects.create(
            title=validated_data['title'],
            description=validated_data.get('description', ''),
            user=self.context['request'].user
        )
        return task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user