from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CateringBooking(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    event_date = models.DateField()
    menu_items = models.ManyToManyField(MenuItem)
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Booking for {self.customer_name} on {self.event_date}'
