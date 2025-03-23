from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from .models import About, Project, Feature, Client

class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        # Allow adding only if no About object exists
        return not About.objects.exists()
    
    def save_model(self, request, obj, form, change):
        # If we're adding a new object and one already exists, update the existing one
        if not change and About.objects.exists():
            existing_about = About.objects.first()
            existing_about.title = obj.title
            existing_about.description = obj.description
            existing_about.save()
        else:
            super().save_model(request, obj, form, change)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'preview_image', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'preview_image')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'type')
        }),
        ('Media', {
            'fields': ('image', 'preview_image', 'preview_link', 'preview_video_link')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "No Image"
    
    preview_image.short_description = 'Image Preview'

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview_image', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'preview_image')
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Media', {
            'fields': ('image', 'preview_image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "No Image"
    
    preview_image.short_description = 'Image Preview'

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'phone', 'rate_stars', 'created_at')
    list_filter = ('rate', 'specialization')
    search_fields = ('name', 'specialization', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'rate_stars')
    fieldsets = (
        (None, {
            'fields': ('name', 'phone', 'specialization', 'rate', 'rate_stars')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def rate_stars(self, obj):
        stars = '★' * obj.rate + '☆' * (5 - obj.rate)
        return format_html('<span style="color: gold;">{}</span>', stars)
    
    rate_stars.short_description = 'Rating'

admin.site.register(About, AboutAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Client, ClientAdmin)
