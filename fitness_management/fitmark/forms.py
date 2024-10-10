import datetime
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *

class ExtendedUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')

class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'detail', 'price', 'image']

class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'start_time', 'end_time', 'capacity']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time >= end_time:
            raise forms.ValidationError("เวลาจบต้องอยู่หลังเวลาเริ่ม")

        return cleaned_data
    
    def clean_date(self):
        date = self.cleaned_data.get('date')

        if date < datetime.date.today():
            raise forms.ValidationError("ไม่สามารถเลือกวันที่ย้อนหลังได้")
        
        return date
