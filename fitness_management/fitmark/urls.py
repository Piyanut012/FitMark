from django.urls import path

from . import views

urlpatterns = [
    path("", views.FirstPageView.as_view(), name="first_page"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("index/", views.index, name="index"),
]