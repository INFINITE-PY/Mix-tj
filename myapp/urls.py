from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('watch/<int:id>/', views.watch, name='watch'),
    path('upload/', views.upload_video, name='upload_video'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]