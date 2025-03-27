from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Property, Collection
from django.shortcuts import get_object_or_404
from geopy.geocoders import Nominatim
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.base import ContentFile
from django.conf import settings


# Create your views here.
@login_required
def add_property(request):
    if request.user.role != 'librarian':
        return redirect(request.META.get('HTTP_REFERER', 'listing_service:property_listing'))

    if request.method == 'POST':
        title = request.POST['title']
        property_type = request.POST['property_type']
        description = request.POST['description']
        location = request.POST['location']
        price = request.POST['price']
        image = request.FILES.get('image')

        property_object = Property.objects.create(
            title=title,
            property_type=property_type,
            description=description,
            location=location,
            price=price,
            image=None,
        )

        if image:
            s3_storage = S3Boto3Storage()
            file_name = f"listing-image/{property_object.id}_{image.name}"
            saved_file_path = s3_storage.save(file_name, ContentFile(image.read()))

            property_object.image = f"{settings.AWS_S3_CUSTOM_DOMAIN}/{saved_file_path}"
            property_object.save()

        return redirect('listing_service:property_listing')

    return render(request, 'listing_service/add_property.html')

	
def property_listing(request):
    properties = Property.objects.all()

    return render(request, 'listing_service/property_listing.html', {"user": request.user, "properties": properties})


def property_details(request, property_id):
    property_object = get_object_or_404(Property, id=property_id)
    geolocator = Nominatim(user_agent="myApp")
    location = geolocator.geocode(property_object.location)

    lat, lon = (location.latitude, location.longitude) if location else (None, None)

    details = {
        "title": property_object.title,
        "image": property_object.image if property_object.image else "",
        "property_type": property_object.property_type,
        "description": property_object.description,
        "location": property_object.location,
        "price": property_object.price,
        "lat": lat,
        "lon": lon,
    }

    return render(request, 'listing_service/property_details.html', {"details": details})


@login_required
def create_collection(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        private = request.POST.get('private') == 'on'
        property_ids = request.POST.getlist('properties')

        collection_object = Collection.objects.create(
            title=title,
            description=description,
            private=private,
            owner=request.user
        )
        collection_object.properties.set(Property.objects.filter(id__in=property_ids))
        collection_object.save()

        return redirect('listing_service:collection_listing')

    properties = Property.objects.all()
    return render(request, 'listing_service/create_collection.html', {'properties': properties})


def collection_listing(request):
    collections = Collection.objects.all()
    return render(request, 'listing_service/collection_listing.html', {'collections': collections})

def collection_details(request, collection_id):
    collection_object = get_object_or_404(Collection, id=collection_id)
    return render(request, 'listing_service/collection_details.html', {'collection': collection_object})
