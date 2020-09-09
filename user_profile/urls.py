from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('update-profile/', views.UpdateProfile.as_view(), name='update_profile'),
    path('update-profile/photo/', views.UpdateProfilePhoto.as_view(), name='update_profile_pic'),
    path('change-password/', views.UpdatePassword.as_view(), name='change_password'),
    path('delete-account/', views.DeleteAccount.as_view(), name='delete_account'),
    # path('<str:username>/', views.UserProfile.as_view(), name='profile'), 
    path('post/ajax/like/', views.likeUnlike, name='like_unlike')
]