from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from .forms import OrderForm
from .models import Bike, Basket, Order


class BikeListView(ListView):
    model = Bike
    template_name = 'shop/bikes.html'
    context_object_name = 'bikes'


class BikeDetailView(DetailView):
    model = Bike
    template_name = 'shop/bike_details.html'
    context_object_name = 'bike'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bike = self.get_object()
        context['form'] = OrderForm() if bike.is_available() else None
        return context

    def update_quantities(self, bike):
        bike.frame.quantity -= 1
        bike.frame.save()

        bike.seat.quantity -= 1
        bike.seat.save()

        bike.tire.quantity -= 2
        bike.tire.save()

        if bike.has_basket:
            basket = Basket.objects.first()
            basket.quantity -= 1
            basket.save()

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            bike = self.get_object()

            with transaction.atomic():
                self.update_quantities(bike)

                order = form.save(commit=False)
                order.status = 'P'
                order.bike = bike
                order.save()

            return redirect('order_success', pk=order.pk)

        return self.get(request, *args, **kwargs)


class OrderSuccessView(DetailView):
    model = Order
    template_name = 'shop/order_success.html'
    context_object_name = 'order'
