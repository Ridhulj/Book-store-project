from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']

        # Check if username or email already exists
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already in use.')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                user.save()
            return redirect('login')
        else:
            messages.info(request,'This password does not match')
            return redirect('register')

    return render(request, 'accounts/register.html')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.is_staff:  # Check if the user is an admin
                return redirect('booklist')  # Replace with your admin page URL
            else:
                return redirect('userbook_list')  # Replace with your user page URL
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout_view(request):
    auth.logout(request)  # Log out the user
    return redirect('login')  # Redirect to login page after logout

# Homepage View
def homepage(request):
    return render(request, 'accounts/homepage.html')  # Create a homepage.html template
