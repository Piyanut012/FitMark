from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Membership(models.Model):
    name = models.CharField(max_length=50)
    detail = models.TextField(null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    
    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    membership = models.ForeignKey(
        Membership,
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    expertise = models.CharField(max_length=30, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Class(models.Model):
    name = models.CharField(max_length=50)
    detail = models.TextField(null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='class_images/', null=True, blank=True)
    trainer = models.ForeignKey(
        Trainer, 
        on_delete=models.CASCADE, 
    )

    def __str__(self):
        return self.name
    
class Schedule(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField()
    booked_seats = models.PositiveIntegerField(default=0)
    class_instacne = models.ForeignKey(
        Class, 
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.class_instacne.name} on {self.date}"

class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Booking by {self.customer} on {self.created_at}"
    
class Manager(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

