from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group

from django.contrib.auth.models import User
from applications.models import Renewal, ScholarshipApplication
from .models import StudentProfile


# =========================
# HOME PAGE
# =========================
def index(request):
    return render(request, 'index.html')


# =========================
# GROUP CHECK FUNCTIONS
# =========================
def is_student(user):
    return user.groups.filter(name='Student').exists()
def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


# =========================
# DASHBOARDS
# =========================

@user_passes_test(is_student)
def student_dashboard(request):
    profile = getattr(request.user, 'studentprofile', None)
    applications = ScholarshipApplication.objects.filter(student=request.user)
    renewals = Renewal.objects.filter(student=request.user)
    
    has_approved = applications.filter(status='Approved').exists()

    return render(request, 'student/dashboard.html', {
        'profile': profile,
        'applications': applications,
        'renewals': renewals,
        'has_approved': has_approved
    })


@user_passes_test(is_teacher)
def teacher_dashboard(request):
    applications = ScholarshipApplication.objects.all()

    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        action = request.POST.get('action')
        application = ScholarshipApplication.objects.get(id=app_id)
        application.status = action
        application.save()

    return render(request, 'teacher/dashboard.html', {'applications': applications})

def admin_dashboard(request):
    applications = ScholarshipApplication.objects.all().order_by('-submitted_at')
    renewals = Renewal.objects.all().order_by('-submitted_at')

    return render(request, 'admin/dashboard.html', {
        'applications': applications,
        'renewals': renewals
    })



# =========================
# FORMS
# =========================

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        student_id = request.POST.get('student_id')
        course = request.POST.get('course')
        year_level = request.POST.get('year_level')

        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {
                'error': 'email already exists'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        student_group, created = Group.objects.get_or_create(name='Student')
        user.groups.add(student_group)

        StudentProfile.objects.create(
            user=user,
            student_id=student_id,
            course=course,
            year_level=year_level
        )

        return redirect('login')

    return render(request, 'accounts/register.html')

def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.groups.filter(name='Admin').exists():
                return redirect('admin_dashboard')
            elif user.groups.filter(name='Teacher').exists():
                return redirect('teacher_dashboard')
            elif user.groups.filter(name='Student').exists():
                return redirect('student_dashboard')

        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

# =========================
# CRUD OPERATIONS FOR APPLICATIONS
# =========================

@user_passes_test(is_admin)
def update_application_status(request, app_id):
    application = get_object_or_404(ScholarshipApplication, id=app_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        application.status = status
        application.save()

    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def delete_application(request, app_id):
    application = get_object_or_404(ScholarshipApplication, id=app_id)
    application.delete()
    return redirect('admin_dashboard')

# =========================
# CRUD OPERATIONS FOR RENEWALS
# =========================

@user_passes_test(is_admin)
def update_renewal_status(request, renewal_id):
    renew = get_object_or_404(Renewal, id=renewal_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        renew.status = status
        renew.save()

    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def delete_renewal(request, renewal_id):
    renew = get_object_or_404(Renewal, id=renewal_id)
    renew.delete()
    return redirect('admin_dashboard')











