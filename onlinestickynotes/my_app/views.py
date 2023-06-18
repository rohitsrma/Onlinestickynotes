from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import *


@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        note_content = request.POST.get('note_content')
        if note_content:
            Note.objects.create(user=request.user, content=note_content)
        return redirect('home')  # Redirect to the home page after submitting the note
    notes = Note.objects.order_by('-timestamp')  # Fetch all notes ordered by timestamp

    paginator = Paginator(notes, 25)  # Display 5 notes per page

    page_number = request.GET.get('page')  # Get the current page number from the request's query parameters
    page_obj = paginator.get_page(page_number)  # Get the Page object for the current page

    context = {
        'page_obj': page_obj
    }
    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        else:
            try:
                validate_password(password1, user=User(email=email))
            except ValidationError as validation_error:
                messages.error(request, validation_error)
            else:
                if User.objects.filter(username=email).exists():
                    messages.error(request, "You are already registered, please login")
                    return redirect('login')
                else:
                    user = User.objects.create_user(username=email, email=email, password=password1)
                    user.save()
                    auth_login(request, user)
                    messages.success(request, "Signup successful. You are now logged in.")
                    return redirect('home')

    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')

        user = authenticate(request, username=email, password=password1)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'login.html')
