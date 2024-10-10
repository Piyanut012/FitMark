from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

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
        context = {
            "user": trainer,
            "classes": classes
        }
        return render(request, 'ManageClasses.html', context)
    
    def post(self, request):

        if request.POST.get('_method') == 'POST':
            form = ClassForm(request.POST)
            if form.is_valid():
                class_instance = form.save(commit=False)
                class_instance.trainer = request.user.trainer
                class_instance.save()
                return redirect('manage_classes')
            else:
                print(form.errors)
            
            return render(request, 'ManageClasses.html', {'form': form})
        
        elif request.POST.get('_method') == 'PUT':
            class_id = request.POST.get('class_id')
            print(class_id)
            class_instance = get_object_or_404(Class, id=class_id)
            form = ClassForm(request.POST ,instance=class_instance)

            if form.is_valid():
                form.save()
                messages.success(request, "Class edited successfully")
                return JsonResponse({"success": True})
            else:
                # Return JSON response with form errors and mark success as False
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
        
        elif request.POST.get('_method') == 'DELETE':
            class_id = request.POST.get('class_id')
            class_instance = get_object_or_404(Class, id=class_id)
            class_instance.delete()
            return redirect('manage_classes')
    
    # def put(self, request):
    #     class_id = request.POST.get('edit_class_id')
    #     print(class_id)
    #     class_instance = get_object_or_404(Class, id=class_id)
    #     form = ClassForm(request.POST ,instance=class_instance)

    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "Class edited successfully")
    #         return JsonResponse({"success": True})
    #     else:
    #         # Return JSON response with form errors and mark success as False
    #         return JsonResponse({"success": False, "errors": form.errors}, status=400)

class ClassesScheduleView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        trainer = request.user.trainer
        classes = Class.objects.filter(trainer=trainer)
        context = {
            "user": trainer,
            "classes": classes
        }

        return render(request, 'ClassesSchedule.html', context)
    
class ClassScheduleView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, class_id):
        class_instacne = get_object_or_404(Class, id=class_id)
        schedules = Schedule.objects.filter(class_instacne=class_instacne)
        
        # สร้าง list ของวันที่ที่มี schedule
        schedule_data = [{
            'date': schedule.date.isoformat(),  # เก็บวันในรูปแบบ YYYY-MM-DD
            'start_time': schedule.start_time.strftime('%H:%M'),
            'end_time': schedule.end_time.strftime('%H:%M'),
            'booked_seats': schedule.booked_seats,
            'capacity': schedule.capacity
        } for schedule in schedules]

        return JsonResponse(schedule_data, safe=False)
    
    def post(self, request):
        class_id = request.POST.get('class_instance_id')
        print(class_id)
        class_instance = get_object_or_404(Class, id=class_id)
        form = ScheduleForm(request.POST)
        
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.class_instacne = class_instance
            schedule.save()
            messages.success(request, "Schedule added successfully")
            return JsonResponse({"success": True})
        else:
            # Return JSON response with form errors and mark success as False
            return JsonResponse({"success": False, "errors": form.errors}, status=400)


     






