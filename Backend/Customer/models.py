from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='customer_photos/', blank=True, null=True)


class Contact(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    email = models.EmailField()
    mobile = models.CharField(max_length=255)
    

    def __str__(self):
        return self.name