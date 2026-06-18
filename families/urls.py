from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('vasti-patrak/', views.family_directory, name='family_directory'),
    path('family/<int:pk>/', views.family_detail, name='family_detail'),
    path('family/<int:pk>/pdf/', views.family_pdf, name='family_pdf'),
    path('contact/', views.contact_page, name='contact'),

    # User family management (login required)
    path('my-family/', views.my_family, name='my_family'),
    path('my-family/register/', views.my_family_register, name='my_family_register'),
    path('my-family/<int:pk>/edit/', views.my_family_edit, name='my_family_edit'),
    path('my-family/<int:pk>/members/', views.my_family_members, name='my_family_members'),
    path('my-family/<int:family_pk>/members/<int:member_pk>/delete/', views.my_family_member_delete, name='my_family_member_delete'),
]
