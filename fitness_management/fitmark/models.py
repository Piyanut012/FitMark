from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Membership(models.Model):
    name = models.CharField(max_length=50)
    detail = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)
    quota = models.IntegerField(default=0)
    
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
    membership_expiry_date = models.DateField(null=True, blank=True)
    free_classes_remaining = models.IntegerField(default=0) 
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def check_membership_expired(self):
        # เช็คว่าสมาชิกหมดอายุหรือไม่
        if self.membership and self.membership_expiry_date:
            if date.today() > self.membership_expiry_date:
                self.membership = None
                self.free_classes_remaining = 0
                self.membership_expiry_date = None
                self.save()
                return True
        return False
    
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
    price = models.IntegerField(default=0)
    image = models.URLField(max_length=200, null=True, blank=True)
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
    capacity = models.IntegerField()
    booked_seats = models.IntegerField(default=0)
    class_instacne = models.ForeignKey(
        Class, 
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.class_instacne.name} on {self.date}"
    
    def delete(self, *args, **kwargs):
        # คืนค่า free_classes_remaining ให้กับทุกๆ Customer ที่จองคลาสนี้
        bookings = Booking.objects.filter(schedule=self)
        for booking in bookings:
            if booking.customer.membership:
                booking.customer.free_classes_remaining += 1
                booking.customer.save()
        super().delete(*args, **kwargs)

class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    used_quota = models.BooleanField(default=False)
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
    
    def save(self, *args, **kwargs):
        # ตรวจสอบสมาชิก
        if self.customer.membership:
            if self.customer.free_classes_remaining > 0:
                self.used_quota = True
                self.customer.free_classes_remaining -= 1
                print(self.customer.free_classes_remaining)
                self.customer.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.customer.membership:
            if self.customer.free_classes_remaining > 0:
                self.customer.free_classes_remaining += 1
                self.customer.save()

        super().delete(*args, **kwargs)

