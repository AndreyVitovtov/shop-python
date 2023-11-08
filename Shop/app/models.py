from django.db import models
from django.utils import text, timezone
from accounts.models import Customer


# Create your models here.

class Category(models.Model):
    title = models.TextField()

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    title = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(unique=True, max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.title)
        super().save()


class Product(models.Model):
    title = models.TextField()
    slug = models.CharField(unique=True, max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='app/images/')
    description = models.TextField()
    price = models.FloatField()
    count = models.IntegerField()
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.title)
        super().save()


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    count = models.IntegerField(default=1)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return self.order.customer.username
