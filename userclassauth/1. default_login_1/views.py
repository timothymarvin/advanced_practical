from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from . forms import registrationForm
from django.db.models import Q

# Create your views here.

@login_required
def home(request):
    page="home"
    print('Home page')
    return render(request, 'home.html', {'page':page})


def registerUser(request):
    page = 'register'

    if request.user.is_authenticated:
        return redirect('home')

    registration = registrationForm()

    if request.method == 'POST':
        registrationData = registrationForm(request.POST)

        if registrationData.is_valid():
            new_user = registrationData.save(commit=False)
            new_user.username = new_user.username.lower()
            new_user.save()
            login(request, new_user)

            return redirect('home')
        else:
            messages.error(
                request, 'ERROR:  Failed to register User')

    else:
        messages.error(request, 'ERROR:  Submit form using mmethod \"POST\"')

    context = {'page': page, 'registrationForm': registration}
    return render(request, 'userRegistration.html', context)


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username_or_email = request.POST['username_or_email'].lower()
        password = request.POST['password1']

        try:
            user = User.objects.get(
                Q(username=username_or_email) | Q(email=username_or_email))
            db_user = authenticate(
                request, username=user.username, password=password)
            if db_user is not None:
                login(request, db_user)
                return redirect('home')

            else:
                messages.error(
                    request, "ERROR: invalid username or password, please check the login details and try again.")

        except User.DoesNotExist:
            messages.error(
                request, "ERROR: invalid login credentials, please try agin.")

    context = {'page': page}
    return render(request, 'userLogin.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
