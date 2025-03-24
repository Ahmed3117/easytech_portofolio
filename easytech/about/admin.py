from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import About, Project, Feature, Client

# Customize admin site
admin.site.site_header = "EasyTech Portfolio Admin"
admin.site.site_title = "EasyTech Portfolio Admin Portal"
admin.site.index_title = "Welcome to EasyTech Portfolio Admin Portal"

class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    save_on_top = True
    
    def short_description(self, obj):
        if len(obj.description) > 100:
            return obj.description[:100] + "..."
        return obj.description
    short_description.short_description = "Description"
    
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
    list_display = ('title', 'type', 'preview_image', 'preview_links', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'preview_image')
    list_per_page = 20
    save_on_top = True
    date_hierarchy = 'created_at'
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
            return format_html('<img src="{}" width="100" height="auto" style="border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);" />', obj.image.url)
        return "No Image"
    
    def preview_links(self, obj):
        links = []
        if obj.preview_link:
            links.append(format_html('<a href="{}" target="_blank" class="button" style="margin-right: 5px;">Website</a>', obj.preview_link))
        if obj.preview_video_link:
            links.append(format_html('<a href="{}" target="_blank" class="button">Video</a>', obj.preview_video_link))
        
        if links:
            return mark_safe(''.join(links))
        return "No links"
    
    preview_image.short_description = 'Image Preview'
    preview_links.short_description = 'Preview Links'

class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview_image', 'short_description', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'preview_image')
    list_per_page = 20
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': ('title', 'description'),
            'description': 'Enter the feature details here'
        }),
        ('Media', {
            'fields': ('image', 'preview_image'),
            'description': 'Upload an image that represents this feature'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def short_description(self, obj):
        if len(obj.description) > 70:
            return obj.description[:70] + "..."
        return obj.description
    short_description.short_description = "Description"
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" style="border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);" />', obj.image.url)
        return "No Image"
    
    preview_image.short_description = 'Image Preview'

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'phone', 'rate_stars', 'created_at')
    list_filter = ('rate', 'specialization', 'created_at')
    search_fields = ('name', 'specialization', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'rate_stars')
    list_per_page = 25
    save_on_top = True
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('name', 'phone', 'specialization')
        }),
        ('Rating', {
            'fields': ('rate', 'rate_stars'),
            'description': 'Rate the client from 1 to 5 stars'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def rate_stars(self, obj):
        stars = '★' * obj.rate + '☆' * (5 - obj.rate)
        return format_html('<span style="color: gold; font-size: 18px;">{}</span>', stars)
    
    rate_stars.short_description = 'Rating'

# Register admin models
admin.site.register(About, AboutAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Client, ClientAdmin)
