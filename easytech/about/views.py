from django.shortcuts import render
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import About, Project, Feature, Client
from .serializers import (
    AboutSerializer, ProjectSerializer, 
    FeatureSerializer, ClientSerializer
)

# Create your views here.

class PortfolioDataView(APIView):
    """
    View to collect all data needed for portfolio display in a single endpoint.
    Returns the About information, Projects, and Features in a single response.
    """
    def get(self, request, format=None):
        # Get the about information (single instance)
        about = About.objects.first()
        about_data = AboutSerializer(about).data if about else {}
        
        # Get all projects with ordering
        projects = Project.objects.all().order_by('-created_at')
        projects_data = ProjectSerializer(projects, many=True).data
        
        # Get all features with ordering
        features = Feature.objects.all().order_by('title')
        features_data = FeatureSerializer(features, many=True).data
        
        # Combine all data
        return Response({
            'about': about_data,
            'projects': projects_data,
            'features': features_data,
        })

class AboutListView(generics.ListAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    
    def list(self, request, *args, **kwargs):
        # Get the single About object or create an empty one
        instance = About.objects.first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

class ProjectTypesView(APIView):
    def get(self, request, format=None):
        return Response(dict(Project.PROJECT_TYPES))

class FeatureListView(generics.ListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at']
    ordering = ['title']

class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rate', 'specialization']
    search_fields = ['name', 'specialization']
    ordering_fields = ['rate', 'name', 'created_at']
    ordering = ['-rate', 'name']
