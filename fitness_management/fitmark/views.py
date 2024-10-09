from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse

class FirstPageView(View):

    def get(self, request):
        return render(request, 'first_page.html', {})

class LoginView(View):

    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": None})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Check role
            if hasattr(user, 'customer'):
                return redirect('booking')
            elif hasattr(user, 'trainer'):
                return redirect('manage_classes')
            
        return render(request, 'login.html', {"form": form})

class LogoutView(View):
    
    def get(self, request):
        logout(request)
        return redirect('login')
    
class SignUpView(View):
    
    def get(self, request):
        form = ExtendedUserCreationForm()
        return render(request, 'signup.html', {"form": form})

    def post(self, request):
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create Customer object
            Customer.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
            )
            return redirect('login')
        return render(request, 'signup.html', {'form': form})


class BookingView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        customer = request.user.customer
        classes = Class.objects.all()
        context = {
            "user": customer,
            "classes": classes
        }
        # form = BookingForm()
        return render(request, 'booking.html', context)


class ManageClasses(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        trainer = request.user.trainer
        classes = Class.objects.filter(trainer=trainer)
        form = ClassForm()
        context = {
            "user": trainer,
            "classes": classes,
            "form": form
        }
        return render(request, 'ManageClasses.html', context)
    
    def post(self, request):
        form = ClassForm(request.POST, request.FILES)
        if form.is_valid():
            class_instance = form.save(commit=False)
            class_instance.trainer = request.user.trainer
            class_instance.save()
            return redirect('manage_classes')
        else:
            print(form.errors)
        
        return render(request, 'ManageClasses.html', {'form': form})


# def index(request):
#     context = {}
#     return render(request, 'booking.html', context)



