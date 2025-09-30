from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('vidownload/<str:id>/', views.progress, name='vidownload')
]