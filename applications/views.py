from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ScholarshipApplication
from .models import Renewal

# Helper functions
def is_student(user):
    return user.groups.filter(name='Student').exists()

def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()

def is_admin(user):
    return user.groups.filter(name='Admin').exists()


# =========================
# Student: Apply for scholarship
# =========================
@user_passes_test(is_student)
def apply_scholarship(request):
    if request.method == 'POST':
        gpa = request.POST.get('gpa')
        document = request.FILES.get('document')

        scholarship = ScholarshipApplication.objects.filter(
            student=request.user,
            status='Approved'
        ).first()

        if scholarship:
            return redirect('student_dashboard')
        else:
            ScholarshipApplication.objects.create(
                student=request.user,
                gpa=gpa,
                document=document
            )
            return redirect('student_dashboard')

    return render(request, 'applications/apply.html')

# =========================
# Student: Apply for renewal
# =========================
@user_passes_test(is_student)
def apply_renewal(request):
    scholarship = ScholarshipApplication.objects.filter(
        student=request.user,
        status='Approved'
    ).first()

    latest_renewal = Renewal.objects.filter(
        student=request.user,
        scholarship=scholarship
    ).order_by('-submitted_at').first()


    if not scholarship:
        return redirect('student_dashboard')
    
    if latest_renewal and latest_renewal.status != 'Approved':
        return redirect('student_dashboard')

    if request.method == 'POST':
        semester = request.POST.get('semester')
        gpa = request.POST.get('gpa')
        document = request.FILES.get('document')

        if Renewal.objects.filter(
            student=request.user,
            scholarship=scholarship,
            semester=semester
        ).exists():
            return redirect('student_dashboard')

        Renewal.objects.create(
            student=request.user,
            scholarship=scholarship,
            semester=semester,
            gpa=gpa,
            document=document
        )

        return redirect('student_dashboard')

    return render(request, 'applications/apply_renewal.html', {
        'scholarship': scholarship
    })

# =========================
# Teacher/Admin: Review applications
# =========================
@user_passes_test(lambda u: is_teacher(u) or is_admin(u))
def review_applications(request):
    applications = ScholarshipApplication.objects.all()

    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        action = request.POST.get('action')
        application = ScholarshipApplication.objects.get(id=app_id)
        application.status = action
        application.save()

    return render(request, 'applications/review_applications.html', {'applications': applications})


