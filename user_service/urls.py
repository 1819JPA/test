from django.urls import path
from .views import edit_profile, librarian_dashboard, update_user_role, \
    manage_users  # Import the view

app_name = "user_service"  # This enables the namespace "user_service"

urlpatterns = [
    path("librarian-dashboard/", librarian_dashboard, name="librarian_dashboard"),
    path("manage-users/", manage_users, name="manage_users"),  # user managing page
    path("update-role/<int:user_id>/", update_user_role, name="update_user_role"),  # role change
    path("profile/", edit_profile, name="edit_profile"),
]