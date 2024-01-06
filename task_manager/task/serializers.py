# serializers.py
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'slug', 'description', 'priority', 'due_date', 'completed', 'created_at', 'updated_at', 'user', 'image', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        task = Task.objects.create(**validated_data)

        for image_data in images_data:
            task_image = TaskImage.objects.create(task=task, image=image_data)

        return task
