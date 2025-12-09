from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages


# Create your views here.
def student_index(request):
    return render(request, 'student_html/student_index.html')

def student_signUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        repeat_pass = request.POST.get('repeat_pass')

        if repeat_pass == password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exist')
                return redirect('signUp')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exist')
                return redirect('signUp')
            else:
                User.objects.create_user(username=username,email=email,password=password)
                return redirect('logIn')
        else:
            messages.info(request, 'Password not the same')
    return render(request, 'student_html/student_signUp.html')

def student_logIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/student')
        else:
            messages.info(request, 'Credential invalid!')

    return render(request, 'student_html/student_logIn.html')

def student_logout(request):
    auth.logout(request)
    return redirect('/')

def student_register_success(request):
    return render(request, 'student_html/student_register_success.html')

def dashboard(request):
    return render(request, 'student_html/dashboard.html')


