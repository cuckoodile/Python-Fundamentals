from django.urls import path

from . import views

urlpatterns = [
    # auth
    path('auth/login/', views.LoginAPIView.as_view()),
    path('auth/logout/', views.LogoutAPIView.as_view()),
    path('auth/me/', views.MeAPIView.as_view()),

    # users
    path('users/', views.BaseUserListCreateAPIView.as_view()),
    path('users/<int:pk>/', views.BaseUserRetrieveUpdateDestroyAPIView.as_view()),

    # contact types
    path('contact-types/', views.ContactTypeListCreateAPIView.as_view()),
    path('contact-types/<int:pk>/', views.ContactTypeRetrieveUpdateDestroyAPIView.as_view()),

    # contacts
    path('contacts/', views.ContactListCreateAPIView.as_view()),
    path('contacts/<int:pk>/', views.ContactRetrieveUpdateDestroyAPIView.as_view()),
]
