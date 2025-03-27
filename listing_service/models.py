from django.db import models
from user_service.models import CustomUser

# Create your models here.
class Property(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField(blank=True, null=True)
    property_type = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.title
    
class Collection(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField(blank=True, null=True)
    properties = models.ManyToManyField(Property)
    description = models.TextField()
    private = models.BooleanField(default = False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title