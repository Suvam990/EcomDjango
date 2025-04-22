from django.db import models
# from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=20)
    # slug = models.SlugField(unique=True, blank=True,default='temp-slug')


    # def save(self,*args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(slugify.name)
    #     super().save(*args, **kwargs)    

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()