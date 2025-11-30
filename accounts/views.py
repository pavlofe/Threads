from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from .models import Profile


from accounts.forms import LoginForm, RegisterForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class RegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        age = request.POST.get('age')

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )

        Profile.objects.create(
            user=user,
            gender=gender,
            phone=phone
        )

        login(request, user)
        return redirect('home')

    return render(request, 'accounts/register.html')
