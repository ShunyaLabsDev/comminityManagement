from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='events'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
]
