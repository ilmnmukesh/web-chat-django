
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Default, name='login'),
    path('forgot/', views.ForgotPassword, name='forgot_password'),
    path('update_name/', views.updateName, name='update_name'),
    path('update_image/', views.updateImage, name='update_image'),
]