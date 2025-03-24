from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class About(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "About Information"
        verbose_name_plural = "About Information"

class Project(models.Model):
    PROJECT_TYPES = (
        ('website', 'Website'),
        ('mobile_app', 'Mobile App'),
        ('desktop_app', 'Desktop App'),
        ('ecommerce', 'E-Commerce'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(max_length=1000,blank=True, null=True)
    image = models.ImageField(upload_to='projects/')
    preview_link = models.URLField(blank=True, null=True)
    preview_video_link = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='website')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

class Feature(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000,blank=True, null=True)
    image = models.ImageField(upload_to='features/',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        verbose_name = "Feature"
        verbose_name_plural = "Features"

class Client(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    specialization = models.CharField(max_length=200)
    image = models.ImageField(upload_to='clients/', blank=True, null=True)
    rate = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-rate', 'name']
        verbose_name = "Client"
        verbose_name_plural = "Clients"
