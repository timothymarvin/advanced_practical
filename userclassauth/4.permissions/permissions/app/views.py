from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import registrationForm
from .models import CustomUser

# Custom function to check if the user is staff
def staff_required(user):
    return user.is_staff

# Custom function to check if the user is superuser
def superuser_required(user):
    return user.is_superuser

# Home view
@login_required
def home(request):
    page = "home"
    return render(request, 'home.html', {'page': page})

# Register User view
def registerUser(request):
    page = 'register'
    if request.user.is_authenticated:
        return redirect('home')

    registration = registrationForm()

    if request.method == 'POST':
        registrationData = registrationForm(request.POST)
        if registrationData.is_valid():
            new_user = registrationData.save(commit=False)
            new_user.username = new_user.username.lower()  # Normalize username
            new_user.save()
            login(request, new_user)
            return redirect('home')
        else:
            messages.error(request, 'ERROR: Failed to register User')

    context = {'page': page, 'registrationForm': registration}
    return render(request, 'userRegistration.html', context)

# Login User view
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username_or_email = request.POST['username_or_email'].lower()
        password = request.POST['password1']
        try:
            user = CustomUser.objects.get(
                Q(username=username_or_email) | Q(email=username_or_email))
            db_user = authenticate(request, username=user.username, password=password)
            if db_user is not None:
                login(request, db_user)
                return redirect('home')
            else:
                messages.error(request, "ERROR: invalid username or password.")
        except CustomUser.DoesNotExist:
            messages.error(request, "ERROR: invalid login credentials.")

    context = {'page': page}
    return render(request, 'userLogin.html', context)

# Logout User view
def logoutUser(request):
    logout(request)
    return redirect('login')

# View Data (normal users can view)
@login_required
@user_passes_test(lambda u: u.has_perm('view_data') or u.is_staff or u.is_superuser)
def view_data(request):
    return render(request, 'app/view_data.html')

# Edit Data (only staff or superusers can edit)
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def edit_data(request):
    return render(request, 'app/edit_data.html')

# Delete Data (only superusers can delete)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_data(request):
    return render(request, 'app/delete_data.html')
