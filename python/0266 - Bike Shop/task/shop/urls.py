from django.urls import path

from shop.views import BikeDetailView, OrderSuccessView

urlpatterns = [
    path('bikes/<int:pk>/', BikeDetailView.as_view(), name='bike_details'),
    path('order/<int:pk>/', OrderSuccessView.as_view(), name='order_success'),
]
