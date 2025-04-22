from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=10)

    def register(self):
        self.save()

    def isExists(self):
        if Customer.objects.filter(phone=self.phone):
            return True
        else:
            return False