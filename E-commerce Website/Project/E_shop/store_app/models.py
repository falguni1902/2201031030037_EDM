from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField


class Categories(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}"


class Brand(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}"


class Color(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Filter_Price(models.Model):
    FILTER_PRICE = (
        ('1000 TO 10000', '1000 TO 10000'),
        ('10000 TO 20000', '1000 TO 20000'),
        ('20000 TO 30000', '20000 TO 30000'),
        ('30000 TO 40000', '30000 TO 40000'),
        ('40000 TO 50000', '40000 TO 50000'),
    )

    price = models.CharField(choices=FILTER_PRICE, max_length=64)

    def __str__(self):
        return f"{self.price}"


class Product(models.Model):
    CONDITION = (('New', 'New'), ('Old', 'Old'))
    STOCK = (('In Stock', 'In Stock'), ('Out Of Stock', 'Out Of Stock'))
    STATUS = (('Publish', 'Publish'), ('Draft', 'Draft'))

    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Filter_Price, on_delete=models.CASCADE)

    unique_id = models.CharField(unique=True, max_length=256, null=True, blank=True)
    image = models.ImageField(upload_to='Product_images/img')
    name = models.CharField(max_length=256)
    price = models.IntegerField()
    condition = models.CharField(choices=CONDITION, max_length=128)
    information = RichTextField(null=True)
    description = RichTextField(null=True)
    stock = models.CharField(choices=STOCK, max_length=256)
    status = models.CharField(choices=STATUS, max_length=256)
    created_date = models.DateTimeField(default=timezone.now)

    # def save(self, *args, **kaargs):
    #     if self.unique_id is None and self.created_date and self.id:
    #         self.unique_id = self.created_date.strtime('14%y%m%d25').str(self.id)
    #     return super().save(*args, **kaargs)

    def save(self, *args, **kwargs):
        if not self.unique_id and self.created_date and self.id:
            self.unique_id = self.created_date.strftime('14%y%m%d25') + str(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Images(models.Model):
    images = models.ImageField(upload_to='Product_images/img')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=256)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Contact_us(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)
    subject = models.CharField(max_length=256)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=256)
    lastname = models.CharField(max_length=256)
    countryname = models.CharField(max_length=128)
    address = models.TextField()
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    postcode = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=128)
    additional_imfo = models.TextField()
    amount = models.CharField(max_length=64)
    payment_id = models.CharField(max_length=128, null=True, blank=True)
    paid = models.BooleanField(default=False, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    products = models.CharField(max_length=256)
    image = models.ImageField(upload_to='Product_images/Order_img')
    quantity = models.CharField(max_length=32)
    price = models.CharField(max_length=64)
    total = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.order.user.username}"

