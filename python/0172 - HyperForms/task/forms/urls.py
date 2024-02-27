from django.urls import path

from .views import HomePageView, RegisterView

urlpatterns = [
    path('', HomePageView.as_view(), name='main'),
    path('register/', RegisterView.as_view(), name='register'),
]
