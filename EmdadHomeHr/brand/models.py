from django.db import models

# Create your models here.


class Brand(models.Model):

    name = models.CharField(max_length=100)
    about = models.TextField()
    logo = models.ImageField(upload_to='images/brands', default='images/brands/emdadHomeMainBg.webp')

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=1024)
    stock = models.IntegerField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
