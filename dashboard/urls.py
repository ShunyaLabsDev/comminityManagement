from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('families/', views.family_list, name='dashboard_families'),
    path('families/add/', views.family_add, name='family_add'),
    path('families/<int:pk>/edit/', views.family_edit, name='family_edit'),
    path('families/<int:family_pk>/member/add/', views.member_add, name='member_add'),
    path('events/add/', views.event_add, name='event_add'),
    path('announcements/add/', views.announcement_add, name='announcement_add'),
]
