from django.urls import path
from downloader import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download_video, name='download_video'),
]
