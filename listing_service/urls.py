from django.urls import path
from . import views

app_name = 'listing_service'

urlpatterns = [
    path('', views.property_listing, name="property_listing"),
    path('add/', views.add_property, name="add_property"),
    path('property/<int:property_id>/', views.property_details, name='property_details'),
    path('create/', views.create_collection, name="create_collection"),
    path('collections/', views.collection_listing, name="collection_listing"),
    path('collections/<int:collection_id>/', views.collection_details, name='collection_details'),
]