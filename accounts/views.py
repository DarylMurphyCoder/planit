from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def signup(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('task-list')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            msg = f'Welcome, {user.username}! Your account has been created.'
            messages.success(request, msg)
            return redirect('task-list')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})
