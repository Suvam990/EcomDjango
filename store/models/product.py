from django.db import models
from .category import Category


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    price = models.IntegerField(default=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=250, default='')
    image = models.ImageField(upload_to='upload/products/', blank=True, null=True)





    @staticmethod
    def get_all_product():
        return Product.objects.all()
    

    def __str__(self):
        return self.name

    # @staticmethod
    # def get_all_product_cateory_id(category_id):
    #     if category_id:
    #         return Product.objects.filter(category=category_id)
    #     else:
    #         return Product.get_all_product()
    @classmethod
    def get_all_product_category_id(cls, category_id):
        return cls.objects.filter(category_id=category_id)
 
    # @staticmethod
    # def get_all_product_by_category_slug(slug):
    #     category = Category.objects.filter(slug=slug).first()
    #     if category:
    #         return Product.objects.filter(category=category)
    #     return Product.objects.all()
    def discount_percentage(self):
        if self.original_price > self.price:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            return round(discount, 2)
        return 0 

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='upload/products/', blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} Image"

 

