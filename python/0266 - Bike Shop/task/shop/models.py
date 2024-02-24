from django.db import models


class Frame(models.Model):
    color = models.CharField(max_length=255)
    quantity = models.IntegerField()

    def __str__(self):
        return f'Frame(color={self.color}, quantity={self.quantity})'


class Seat(models.Model):
    color = models.CharField(max_length=255)
    quantity = models.IntegerField()

    def __str__(self):
        return f'Seat(color={self.color}, quantity={self.quantity})'


class Tire(models.Model):
    type = models.CharField(max_length=255)
    quantity = models.IntegerField()

    def __str__(self):
        return f'Tire(type={self.type}, quantity={self.quantity})'


class Basket(models.Model):
    quantity = models.IntegerField()

    def __str__(self):
        return f'Basket(quantity={self.quantity})'


class Bike(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    has_basket = models.BooleanField()

    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    tire = models.ForeignKey(Tire, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)

    def __str__(self):
        return f'Bike(name={self.name}, frame={self.frame}, tire={self.tire}, seat={self.seat}, has_basket={self.has_basket})'

    def is_available(self):
        if self.frame.quantity > 0 and self.seat.quantity > 0 and self.tire.quantity >= 2:
            if not self.has_basket or (self.has_basket and Basket.objects.first().quantity > 0):
                return True
        return False


class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'pending'),
        ('R', 'ready'),
    ]

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order(name={self.name}, surname={self.surname}, phone_number={self.phone_number}, status={self.get_status_display()}, bike={self.bike})'
