from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from .models import *
from .forms import *
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone

class FirstPageView(View):

    def get(self, request):
        return render(request, 'first_page.html', {})
    
class ClassView(View):

    def get(self, request):

        if request.user.is_authenticated:
            if hasattr(request.user, 'customer'):
                return redirect('booking')
            elif hasattr(request.user, 'trainer'):
                return redirect('classes_schedule')

        classes = Class.objects.all()
        return render(request, 'Classes.html', {"classes": classes})

class LoginView(View):

    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Check role
            if hasattr(user, 'customer'):
                return redirect('booking')
            elif hasattr(user, 'trainer'):
                return redirect('classes_schedule')
            
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
            customer_group = Group.objects.get(name='Customer')
            user.groups.add(customer_group)
            return redirect('login')
        return render(request, 'signup.html', {'form': form})

# Trainer
class ManageClasses(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["fitmark.view_class", "fitmark.add_class", "fitmark.change_class", "fitmark.delete_class"]

    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            messages.error(self.request, "คุณต้องเข้าสู่ระบบก่อน")
            return redirect(self.login_url)

        messages.error(self.request, "คุณไม่มีสิทธิ์เข้าถึงหน้านี้")
        return redirect('booking')

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
                messages.success(request, "เพิ่มคลาสสำเร็จ")
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
        
        elif request.POST.get('_method') == 'PUT':
            class_id = request.POST.get('class_id')
            print(class_id)
            class_instance = get_object_or_404(Class, id=class_id)
            form = ClassForm(request.POST ,instance=class_instance)

            if form.is_valid():
                form.save()
                messages.success(request, "แก้ไขคลาสสำเร็จ")
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "errors": form.errors}, status=400)
        
        elif request.POST.get('_method') == 'DELETE':
            class_id = request.POST.get('class_id')
            class_instance = get_object_or_404(Class, id=class_id)
            class_instance.delete()
            messages.success(request, "ลบคลาสสำเร็จ")
            return redirect('manage_classes')

class ClassesScheduleView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["fitmark.view_class"]
    
    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            messages.error(self.request, "คุณต้องเข้าสู่ระบบก่อน")
            return redirect(self.login_url)

        messages.error(self.request, "คุณไม่มีสิทธิ์เข้าถึงหน้านี้")
        return redirect('booking')

    def get(self, request):
        trainer = request.user.trainer
        classes = Class.objects.filter(trainer=trainer)
        context = {
            "user": trainer,
            "classes": classes
        }

        return render(request, 'ClassesSchedule.html', context)
    
class ClassScheduleView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["fitmark.view_schedule", "fitmark.add_schedule", "fitmark.delete_schedule"]

    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            messages.error(self.request, "คุณต้องเข้าสู่ระบบก่อน")
            return redirect(self.login_url)

        messages.error(self.request, "คุณไม่มีสิทธิ์เข้าถึงหน้านี้")
        return redirect('booking')

    def get(self, request, class_id):
        class_instacne = get_object_or_404(Class, id=class_id)
        schedules = Schedule.objects.filter(class_instacne=class_instacne).order_by('start_time')
        
        # สร้าง list ของวันที่ที่มี schedule
        schedule_data = [{
            'id': schedule.id,
            'date': schedule.date.isoformat(),  # เก็บวันในรูปแบบ YYYY-MM-DD
            'start_time': schedule.start_time.strftime('%H:%M'),
            'end_time': schedule.end_time.strftime('%H:%M'),
            'booked_seats': schedule.booked_seats,
            'capacity': schedule.capacity
        } for schedule in schedules]

        return JsonResponse(schedule_data, safe=False)
    
    def post(self, request):
        class_id = request.POST.get('class_instance_id')
        class_instance = get_object_or_404(Class, id=class_id)
        form = ScheduleForm(request.POST)
        
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.class_instacne = class_instance
            schedule.save()
            messages.success(request, "เพิ่มกำหนดการสำเร็จ")
            return JsonResponse({"success": True})
        else:
            # Return JSON response with form errors and mark success as False
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
    
    def delete(self, request, schedule_id):
        schedule = get_object_or_404(Schedule, id=schedule_id)
        schedule.delete()
        messages.success(request, "ลบกำหนดการสำเร็จ")
        return JsonResponse({"success": True})

# Customer
class BookClassView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["fitmark.view_class"]

    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            messages.error(self.request, "คุณต้องเข้าสู่ระบบก่อน")
            return redirect(self.login_url)

        messages.error(self.request, "คุณไม่มีสิทธิ์เข้าถึงหน้านี้")
        return redirect('classes_schedule')
 
    def get(self, request):
        customer = request.user.customer
        classes = Class.objects.all()
        context = {
            "user": customer,
            "classes": classes
        }
        # form = BookingForm()
        return render(request, 'booking.html', context)

class BookClass(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["fitmark.view_schedule", "fitmark.add_booking"]

    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            messages.error(self.request, "คุณต้องเข้าสู่ระบบก่อน")
            return redirect(self.login_url)

        messages.error(self.request, "คุณไม่มีสิทธิ์เข้าถึงหน้านี้")
        return redirect('classes_schedule')

    def get(self, request, class_id):
        class_instacne = get_object_or_404(Class, id=class_id)
        tomorrow = timezone.now().date() + timedelta(days=1)
        schedules = Schedule.objects.filter(
            class_instacne=class_instacne,
            booked_seats__lt=F('capacity'),
            date__gt=tomorrow
        ).exclude(
            booking__customer=request.user.customer  # Exclude schedules already booked by the customer
        ).order_by('start_time')
        
        # สร้าง list ของวันที่ที่มี schedule
        schedule_data = [{
            'id': schedule.id,
            'date': schedule.date.isoformat(),  # เก็บวันในรูปแบบ YYYY-MM-DD
            'start_time': schedule.start_time.strftime('%H:%M'),
            'end_time': schedule.end_time.strftime('%H:%M'),
            'booked_seats': schedule.booked_seats,
            'capacity': schedule.capacity
        } for schedule in schedules]

        return JsonResponse(schedule_data, safe=False)
    
    def post(self, request):
        schedule_id = request.POST.get('schedule_id')
        schedule = get_object_or_404(Schedule, id=schedule_id)
        schedule.booked_seats += 1
        schedule.save()
         # Create a new booking
        booking = Booking.objects.create(
            schedule=schedule,
            customer=request.user.customer
        )
        booking.save()
        messages.success(request, "จองคลาสสำเร็จ")
        return JsonResponse({"success": True})

class MyBookingView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["fitmark.view_booking", "fitmark.delete_booking"]

    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            messages.error(self.request, "คุณต้องเข้าสู่ระบบก่อน")
            return redirect(self.login_url)

        messages.error(self.request, "คุณไม่มีสิทธิ์เข้าถึงหน้านี้")
        return redirect('classes_schedule')

    def get(self, request):
        customer = request.user.customer
        bookings = Booking.objects.filter(customer=customer).order_by('schedule__date', 'schedule__start_time')
        context = {
            "user": customer,
            "bookings": bookings
        }
        return render(request, 'mybooking.html', context)
    
    def delete(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        booking.schedule.booked_seats -= 1
        booking.schedule.save()
        booking.delete()
        messages.success(request, "ยกเลิกการจองสำเร็จ")
        return JsonResponse({"success": True})



     






