from django.db import models
from django.utils import timezone
from datetime import datetime

class User(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'customer'),
        ('manager', 'manager'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES,default='customer')
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=90,default='')
    email=models.EmailField()
    mobile=models.PositiveIntegerField()
    address=models.TextField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=50)
    pincode=models.PositiveIntegerField()
    password=models.CharField(max_length=12)
    profile_pic=models.ImageField(upload_to="profile_pic/")

    def __str__(self):
        return self.fname
	
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Menu(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='food_images/')
    price1 = models.DecimalField(max_digits=8, decimal_places=2)
    price2 = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.category}"
    
class Cart(models.Model):
    food_item=models.ForeignKey(Menu,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)
    time = models.TimeField(default=datetime.now)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name} - {self.user.fname} ({self.date})"
    
class Leave_A_Comment(models.Model):
    name = models.CharField(max_length=100)
    email=models.EmailField()
    message = models.TextField(max_length=100)

    def __str__(self):
        return self.name
    
class Reservation(models.Model):
    name=models.CharField(max_length=90,default='')
    email=models.EmailField()
    mobile=models.PositiveIntegerField()
    person=models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=datetime.now)
    message = models.TextField(max_length=100)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    rating = models.IntegerField(choices=[
        (5, 'Excellent'),
        (4, 'Very Good'),
        (3, 'Good'),
        (2, 'Fair'),
        (1, 'Poor'),
    ])
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.rating}"
    

class Wishlist(models.Model):
    food_item=models.ForeignKey(Menu,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)
    time = models.TimeField(default=datetime.now)

    def __str__(self):
        return self.user.fname+" - "+self.food_item.name

class DeliveryPerson(models.Model):
    name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=100)
    profile_pic=models.ImageField(upload_to="profile_pic/")

    def __str__(self):
        return self.name
                            

class MyOrder(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=90)
    email=models.EmailField()
    phone=models.PositiveIntegerField(null=True)
    address=models.TextField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=50)
    pincode=models.PositiveIntegerField()
    food_item_name = models.CharField(max_length=255)
    price = models.CharField(max_length=400)
    quantity = models.CharField(max_length=400)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=40)
    date=models.DateField(default=datetime.today)
    time = models.TimeField(default=datetime.now)
    delivery_person = models.ForeignKey(DeliveryPerson, null=True, blank=True, on_delete=models.SET_NULL)
    status_choices = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='PENDING')

    def __str__(self):
        return f"{self.fname} - {self.date} x {self.time}"
