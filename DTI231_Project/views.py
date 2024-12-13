from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# หน้า Home
def home(request):
    return render(request, 'Home.html')

# หน้า Sign In
def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # เปลี่ยนเส้นทางไปที่หน้า Profile
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'Sign in.html')

# หน้า Sign Up
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = user.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully. You can now sign in.")
        return redirect('sign-in')
    return render(request, 'Sign up.html')

# หน้า Profile
@login_required
def profile(request):
    return render(request, 'Profile.html', {'username': request.user.username, 'email': request.user.email})

# หน้า Logout
@login_required
def logout_user(request):
    logout(request)
    return redirect('sign-in')
