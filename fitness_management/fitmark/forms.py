import datetime
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *
from django.db.models import F

class ExtendedUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'detail', 'price', 'image']

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price < 0:
            raise forms.ValidationError("ราคาต้องไม่ต่ำกว่า 0")
        elif price > 5000:
            raise forms.ValidationError("ราคาต้องไม่เกิน 5000")

        return price

class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'start_time', 'end_time', 'capacity']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time < datetime.time(6, 0):
            raise forms.ValidationError("เวลาเริ่มต้องไม่ต่ำกว่า 06.00 น.")
        
        if end_time > datetime.time(22, 0):
            raise forms.ValidationError("เวลาจบต้องไม่เกิน 22.00 น.")

        if start_time >= end_time:
            raise forms.ValidationError("เวลาเริ่มต้องอยู่ก่อนเวลาจบ")
        
        # คำนวณความต่างของเวลา
        time_diff = timedelta(
            hours=end_time.hour - start_time.hour, 
            minutes=end_time.minute - start_time.minute
        )

        if time_diff < timedelta(minutes=45):
            raise forms.ValidationError("ช่วงเวลาต้องไม่น้อยกว่า 45 นาที")
        
        # ดึงข้อมูล Schedule ทั้งหมดในวันเดียวกัน
        overlapping_schedules = Schedule.objects.filter(
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if overlapping_schedules.exists():
            raise forms.ValidationError("เวลาที่เลือกทับซ้อนกับกำหนดการอื่นแล้ว")

        return cleaned_data
    
    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')

        if capacity < 1:
            raise forms.ValidationError("จำนวนคนต้องมากกว่า 0")
        elif capacity > 50:
            raise forms.ValidationError("จำนวนคนต้องไม่เกิน 50")

        return capacity


    

