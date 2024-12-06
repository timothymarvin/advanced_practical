from django.urls import path
from . import views

urlpatterns = [
    path('view-data/', views.view_data, name='home'),
    path('edit-data/', views.edit_data, name='edit_data'),
    path('delete-data/', views.delete_data, name='delete_data'),
    # path('', views.home, name='home'),
    path('accounts/register/', views.registerUser, name='register'),
    path('accounts/login/', views.loginUser, name='login'),
    path('accounts/logout/', views.logoutUser, name='logout'),
]
