from django.contrib import admin

from .models import Tire, Frame, Seat, Bike, Order, Basket

models = [Tire, Frame, Seat, Bike, Order, Basket]

for model in models:
    admin.site.register(model)
