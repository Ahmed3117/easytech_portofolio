from rest_framework import serializers
from .models import About, Project, Feature, Client

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'image', 
            'preview_link', 'preview_video_link', 'type', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'title', 'description', 'image', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ClientSerializer(serializers.ModelSerializer):
    rate_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = [
            'id', 'name', 'phone', 'specialization', 'image',
            'rate', 'rate_display', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'rate_display']
    
    def get_rate_display(self, obj):
        return "★" * obj.rate + "☆" * (5 - obj.rate) 