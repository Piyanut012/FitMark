from django.urls import path

from . import views

urlpatterns = [
    path("", views.FirstPageView.as_view(), name="first_page"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    # Customer pages
    path("booking/", views.BookingView.as_view(), name="booking"),

    # Trainer pages
    path("ManageClasses/", views.ManageClasses.as_view(), name="manage_classes"),
    path("ClassesSchedule/", views.ClassesScheduleView.as_view(), name="classes_schedule"),
    path("ClassSchedule/<int:class_id>/", views.ClassScheduleView.as_view(), name="class_schedule"),
    path("ClassSchedule/add/", views.ClassScheduleView.as_view(), name="add_class_schedule"),

    # path("index/", views.index, name="index"),
]

