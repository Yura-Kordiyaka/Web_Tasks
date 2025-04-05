from django.db import models
from django.db.models import JSONField
from restaurant.models import MenuItem


class Cart(models.Model):
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    items = JSONField(default=dict)

    def total_price(self):
        total = 0
        for menu_item_id, quantity in self.items.items():
            try:
                menu_item = MenuItem.objects.get(id=menu_item_id)
                total += menu_item.price * quantity
            except MenuItem.DoesNotExist:
                continue
        return total

    def add_item(self, menu_item_id, quantity):
        if menu_item_id in self.items:
            self.items[menu_item_id] += quantity
        else:
            self.items[menu_item_id] = quantity
        self.save()

    def remove_item(self, menu_item_id):
        if menu_item_id in self.items:
            del self.items[menu_item_id]
            self.save()

    def update_item_quantity(self, menu_item_id, quantity):
        if menu_item_id in self.items:
            self.items[menu_item_id] = quantity
            self.save()


class Order(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    items = models.ManyToManyField('restaurant.MenuItem', through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_time = models.DateTimeField()
    is_delivered = models.BooleanField(default=False)
    delivery_address = models.CharField(max_length=255)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey('restaurant.MenuItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
