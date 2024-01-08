from django.urls import path
from . import views

urlpatterns = [
    path('', views.Detector.as_view(), name='view'),
    path('api', views.DetectorAPI.as_view(), name='api'),
]