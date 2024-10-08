from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

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
            return redirect('index')
        
        return render(request, 'login.html', {"form": form})
    
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


def index(request):
    context = {}
    return render(request, 'booking.html', context)



