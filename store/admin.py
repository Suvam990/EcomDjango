from django.contrib import admin

# Register your models here.
from .models.product import Product,ProductImage
from .models.category import Category
from .models.customer import Customer
from .models.cart import Cart
from .models.order import OrderDetail


# admin.site.register(Product)
admin.site.register(Category)

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'description', 'image']
    # other configurations

@admin.register(ProductImage)
class AdminProductImage(admin.ModelAdmin):
    list_display = ['product', 'image']


@admin.register(Customer)
class AdminCutomer(admin.ModelAdmin):
    list_display=['id','name','phone']

# admin.site.register(Cart)

@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display=['id','phone','product','image','price']



# admin.site.register(Product,AdminProduct)

@admin.register(OrderDetail)
class AdminOrderDetail(admin.ModelAdmin):
    list_display=['id','user','product_name','image','quantity','price','status','order_date']

