from django.shortcuts import render
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import About, Project, Feature, Client
from .serializers import (
    AboutSerializer, ProjectSerializer, 
    FeatureSerializer, ClientSerializer
)

# Create your views here.

class StatsCountView(APIView):
    """
    View to provide count statistics for clients, projects, and projects by type.
    """
    def get(self, request, format=None):
        # Count clients
        client_count = Client.objects.count()
        
        # Count projects
        project_count = Project.objects.count()
        
        # Count projects by type
        project_types_count = Project.objects.values('type').annotate(count=Count('id'))
        
        # Convert to a more readable format
        project_types_stats = {}
        for item in project_types_count:
            # Get the display name for the type
            type_display = dict(Project.PROJECT_TYPES).get(item['type'], item['type'])
            project_types_stats[type_display] = item['count']
            
        # Combine all stats
        stats = {
            'total_clients': client_count,
            'total_projects': project_count,
            'projects_by_type': project_types_stats,
            'features_count': Feature.objects.count(),
        }
        
        return Response(stats)

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
