from django.urls import path
from .views import (
    AboutListView, ProjectListView, FeatureListView, 
    ClientListView, ProjectTypesView, PortfolioDataView,
    StatsCountView
)

# URL patterns for the API
urlpatterns = [
    # Combined portfolio data endpoint
    path('portfolio-data/', PortfolioDataView.as_view(), name='portfolio-data'),
    
    # Statistics count endpoint
    path('stats-count/', StatsCountView.as_view(), name='stats-count'),
    
    # List views for all models
    path('about/', AboutListView.as_view(), name='about-list'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('features/', FeatureListView.as_view(), name='feature-list'),
    path('clients/', ClientListView.as_view(), name='client-list'),
    
    # About info direct endpoint
    path('about-info/', AboutListView.as_view(), name='about-info'),
    
    # Project types endpoint
    path('project-types/', ProjectTypesView.as_view(), name='project-types'),
] 