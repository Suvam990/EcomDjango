from django.db import models


STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
 )
class OrderDetail(models.Model):
    user = models.CharField(max_length=100,default=True)
    product_name = models.CharField(max_length=250)
    image = models.ImageField(blank=True, null=True)
    quantity =models.PositiveIntegerField(default=1)
    price = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending', choices=STATUS_CHOICE)
