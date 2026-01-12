from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group

from django.contrib.auth.models import User
from .models import StudentProfile, ScholarshipApplication,Renewal


# HOME PAGE
def index(request):
    user = request.user.is_authenticated
    return render(request, 'index.html', {'user': user})

# GROUP CHECK FUNCTIONS
def is_student(user):
    return user.groups.filter(name='Student').exists()
def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()
def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def is_teacher_or_admin(user):
    return is_teacher(user) or is_admin(user)

# DASHBOARDS
@user_passes_test(is_student)
def student_dashboard(request):
    applications = ScholarshipApplication.objects.filter(student=request.user)
    renewals = Renewal.objects.filter(student=request.user)
    profile = request.user.studentprofile
    has_approved = applications.filter(status='Approved').exists()
    renewal_pending = renewals.filter(status='Pending').exists()

    return render(request, 'student/dashboard.html', {
        'applications': applications,
        'renewals': renewals,
        'has_approved': has_approved,
        'renewal_pending': renewal_pending,
        'profile': profile
    })
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if 'app_id' in request.POST:
            app = get_object_or_404(ScholarshipApplication, id=request.POST['app_id'])
            app.status = action
            app.save()

        elif 'renewal_id' in request.POST:
            renew = get_object_or_404(Renewal, id=request.POST['renewal_id'])
            renew.status = action
            renew.save()
        return redirect('teacher_dashboard')

    applications = ScholarshipApplication.objects.all().order_by('-submitted_at')
    renewals = Renewal.objects.all().order_by('-submitted_at')

    return render(request, 'teacher/dashboard.html', {
        'applications': applications,
        'renewals': renewals
    })
@user_passes_test(is_admin)
def admin_dashboard(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        # allowed statuses (important for safety)
        if action not in ['Approved', 'Rejected', 'Pending']:
            return redirect('admin_dashboard')

        # Scholarship Application update
        app_id = request.POST.get('app_id')
        if app_id:
            application = get_object_or_404(ScholarshipApplication, id=app_id)
            application.status = action
            application.save()

        # Renewal update
        renewal_id = request.POST.get('renewal_id')
        if renewal_id:
            renewal = get_object_or_404(Renewal, id=renewal_id)
            renewal.status = action
            renewal.save()

        return redirect('admin_dashboard')

    # GET request
    applications = ScholarshipApplication.objects.all().order_by('-submitted_at')
    renewals = Renewal.objects.all().order_by('-submitted_at')

    return render(request, 'admin/dashboard.html', {
        'applications': applications,
        'renewals': renewals,
    })


# Admin: View Users
@user_passes_test(is_admin)
def admin_user(request):
    users = User.objects.all().order_by('username')
    return render(request, 'admin/admin_user.html', {'users': users})

# Admin: View Applications
@user_passes_test(is_admin)
def admin_application(request):
    applications = ScholarshipApplication.objects.all().order_by('-submitted_at')
    return render(request, 'admin/admin_application.html', {'applications': applications})

#admin: View Renewals
@user_passes_test(is_admin)
def admin_renewal(request):
    user = User.objects.all().order_by('username')
    profile = User.studentprofile
    renewals = Renewal.objects.all().order_by('submitted_at')
    return render(request, 'admin/admin_renewals.html', {'user': user, 'profile': profile, 'renewals': renewals})

#admin: View Archive
@user_passes_test(is_admin)
def admin_archive(request):
    applications = ScholarshipApplication.objects.all().order_by('-submitted_at')
    renewals = Renewal.objects.all().order_by('-submitted_at')
    
    return render(request, 'admin/admin_archive.html', {
        'applications': applications,
        'renewals': renewals
    })

# CRUD FOR ADMIN APPLICATIONS - ACCEPT/REJECT
@user_passes_test(is_admin)
def accept_application(request, app_id):
    app = get_object_or_404(ScholarshipApplication, id=app_id)
    app.status = 'Approved'
    app.save()
    messages.success(request, f"Application for {app.firstname} {app.surname} approved.")
    return redirect('admin_applications')
@user_passes_test(is_admin)
def reject_application(request, app_id):
    app = get_object_or_404(ScholarshipApplication, id=app_id)
    app.status = 'Rejected'
    app.save()
    messages.success(request, f"Application for {app.firstname} {app.surname} rejected.")
    return redirect('admin_applications')

#CRUD FOR ADMIN RENEWALS - ACCEPT/REJECT
@user_passes_test(is_admin)
def accept_renewal(request, renewal_id):
    renew = get_object_or_404(Renewal, id=renewal_id)
    renew.status = 'Approved'
    renew.save()
    messages.success(request, f"Renewal for {renew.student.username} approved.")
    return redirect('admin_renewals')
@user_passes_test(is_admin)
def reject_renewal(request, renewal_id):
    renew = get_object_or_404(Renewal, id=renewal_id)
    renew.status = 'Rejected'
    renew.save()
    messages.success(request, f"Renewal for {renew.student.username} rejected.")
    return redirect('admin_renewals')

# Admin: Ban User
@user_passes_test(is_admin)
def ban_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f'User {user.get_full_name} has been banned.')
    return redirect('admin_user')


# SETTINGS FOR STUDENTS PROFILE
@user_passes_test(is_student)
def student_settings(request):
    profile = request.user.studentprofile
    applications = ScholarshipApplication.objects.filter(student=request.user)
    activities = ScholarshipApplication.objects.filter(student=request.user).order_by('-submitted_at')[:5]

    if request.method == 'POST':
        if 'current_password' in request.POST:
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user = request.user

            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
                return redirect('student_settings')

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('student_settings')

            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully. Please log in again.')
            return redirect('login')

        else:
            # Handle profile update
            profile.user.email = request.POST.get('email')
            profile.student_id = request.POST.get('student_id')
            profile.course = request.POST.get('course')
            profile.year_level = request.POST.get('year_level')
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']

            profile.user.save()
            profile.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('student_settings')

    return render(request, 'student/settings.html', {
        'profile': profile,
        'applications': applications,
        'activities': activities
    })

# FORMS
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        student_id = request.POST.get('student_id')
        course = request.POST.get('course')
        year_level = request.POST.get('year_level')
        profile_image = request.FILES.get('profile_image')

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
            year_level=year_level,
            profile_image=profile_image
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

# STUDENT: APPLY FOR SCHOLARSHIP AND RENEWAL
@user_passes_test(is_student)
def apply_scholarship(request):
    if request.method == 'POST':
        existing = ScholarshipApplication.objects.filter(
            student=request.user,
            status='Approved'
        ).first()
        if existing:
            return redirect('student_dashboard')

        previous_school = request.POST.get('previous_school')
        school_year = request.POST.get('school_year')
        surname = request.POST.get('surname')
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        street_no = request.POST.get('street_no')
        city = request.POST.get('city')
        province = request.POST.get('province')
        cellphone = request.POST.get('cellphone')
        semester = request.POST.get('semester')
        strand_course = request.POST.get('strand_course')
        application_date = request.POST.get('application_date')

        proof_identity = request.FILES.get('proof_identity')
        birth_certificate = request.FILES.get('birth_certificate')
        transcript_records = request.FILES.get('transcript_records')
        enrollment_certificate = request.FILES.get('enrollment_certificate')
        good_moral = request.FILES.get('good_moral')
        scholarship_essay = request.FILES.get('scholarship_essay')

        ScholarshipApplication.objects.create(
            student=request.user,
            previous_school=previous_school,
            school_year=school_year,
            surname=surname,
            firstname=firstname,
            middlename=middlename,
            sex=sex,
            age=age,
            street_no=street_no,
            city=city,
            province=province,
            cellphone=cellphone,
            semester=semester,
            strand_course=strand_course,
            application_date=application_date,
            proof_identity=proof_identity,
            birth_certificate=birth_certificate,
            transcript_records=transcript_records,
            enrollment_certificate=enrollment_certificate,
            good_moral=good_moral,
            scholarship_essay=scholarship_essay
        )

        return redirect('student_dashboard')
    profile = request.user.studentprofile
    return render(request, 'accounts/apply.html', {'profile': profile})

@user_passes_test(is_student)
def apply_renewal(request):
    scholarships = ScholarshipApplication.objects.filter(
        student=request.user
    ).first()

    if not scholarships:
        messages.error(request, "No scholarship application found.")
        return redirect('student_dashboard')
    if request.method == 'POST':
        Renewal.objects.create(
            student=request.user,
            scholarship=scholarships,
            semester=request.POST.get('semester'),
            birth_certificate=request.FILES.get('birth_certificate'),
            report_card=request.FILES.get('report_card'),
            enrollment_cert=request.FILES.get('enrollment_cert'),
            good_moral=request.FILES.get('good_moral'),
            id_photo=request.FILES.get('id_photo'),
        )

        messages.success(request, "Renewal submitted successfully.")
        return redirect('student_dashboard')
    profile = request.user.studentprofile

    return render(request, 'accounts/apply_renewal.html', {'profile':profile, 'scholarships':scholarships })

# CRUD FOR ADMIN APPLICATIONS
@user_passes_test(is_admin) # admin only
def delete_application(request, app_id):
    application = get_object_or_404(ScholarshipApplication, id=app_id)
    application.delete()
    return redirect('admin_dashboard')

# # CRUD FOR ADMIN RENEWALS
# @user_passes_test(is_admin) # admin only
# def delete_renewal(request, renewal_id):
#     renew = get_object_or_404(Renewal, id=renewal_id)
#     renew.delete()
#     return redirect('admin_dashboard')

# CRUD FOR STUDENT PROFILES
@user_passes_test(is_student)
def update_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    user = request.user

    if request.method == 'POST':
        # Update profile fields
        profile.student_id = request.POST.get('student_id')
        profile.course = request.POST.get('course')
        profile.year_level = request.POST.get('year_level')
        profile.save()

        # Update User fields
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_password = request.POST.get('password')

        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)

        user.save()

        return redirect('student_dashboard')

    return render(request, 'student/update_profile.html', {
        'profile': profile,
        'user': user
    })
@user_passes_test(is_student)
def delete_profile(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('register')

@user_passes_test(is_student)
def user_documents(request):
    profile = getattr(request.user, 'studentprofile', None)

    applications = ScholarshipApplication.objects.all().order_by('-submitted_at')

    return render(request, 'student/documents.html', {
        'profile': profile,
        'applications': applications,
    })





