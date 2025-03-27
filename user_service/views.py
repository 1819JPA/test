from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.base import ContentFile

from user_service.models import CustomUser  # ✅ Import CustomUser model

# Decorator to check if the user is a Librarian
def is_librarian(user):
    return user.role == "librarian"

@login_required
@user_passes_test(is_librarian)  # Only accessible by Librarians
def librarian_dashboard(request):
    return render(request, "user_service/librarian_dashboard.html")

@login_required
@user_passes_test(is_librarian)  # Only accessible by Librarians
def manage_users(request):
    users = CustomUser.objects.all().order_by("username")  # Retrieve all users
    return render(request, "user_service/manage_users.html", {"users": users})

@login_required
@user_passes_test(is_librarian)  # Only accessible by Librarians
def update_user_role(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        new_role = request.POST.get("role")

        # Prevent a librarian from modifying another librarian's role
        if user.role == "librarian":
            messages.error(request, "You cannot change another librarian's role.")
            return redirect("user_service:manage_users")

        # Only patrons can be promoted to librarians
        if new_role == "librarian" and user.role != "patron":
            messages.error(request, "Only patrons can be promoted to librarians.")
            return redirect("user_service:manage_users")

        if new_role in ["librarian", "patron"]:
            user.role = new_role
            user.save()
            messages.success(request, f"{user.username}'s role has been updated to {new_role}.")

    return redirect("user_service:manage_users")

@login_required
def edit_profile(request):
    user = request.user  # Get the currently logged-in user

    if request.method == 'POST':
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
        profile_image = request.FILES.get("profile_image")

        # Validate password confirmation
        if password and password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("user_service:edit_profile")

        # Update username if provided
        if username:
            if CustomUser.objects.exclude(id=user.id).filter(username=username).exists():
                messages.error(request, "This username is already taken.")
                return redirect("user_service:edit_profile")
            user.username = username

        # Update password (must use set_password)
        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)  # Prevent logout after password change

        # Upload profile image to S3 and save the full URL in the user model
        if profile_image:
            try:
                s3_storage = S3Boto3Storage()  # ✅ Force S3 storage usage
                file_name = f"profile-image/{user.id}_{profile_image.name}"
                saved_file_path = s3_storage.save(file_name, ContentFile(profile_image.read()))

                # Store full S3 URL in the user profile_image field
                user.profile_image = f"{settings.AWS_S3_CUSTOM_DOMAIN}/{saved_file_path}"
            except Exception as e:
                messages.error(request, f"Failed to upload image: {str(e)}")
                return redirect("user_service:edit_profile")

        # Save changes
        user.save()
        messages.success(request, "Profile updated successfully!")

        return redirect("user_service:edit_profile")

    return render(request, "user_service/edit_profile.html", {"user": user})