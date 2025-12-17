from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ScholarshipApplication

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
@login_required
@user_passes_test(is_student)
def apply_scholarship(request):
    if request.method == 'POST':
        gpa = request.POST.get('gpa')
        document = request.FILES.get('document')

        ScholarshipApplication.objects.create(
            student=request.user,
            gpa=gpa,
            document=document
        )
        return redirect('student_applications')

    return render(request, 'applications/apply.html')


# =========================
# Student: View their applications
# =========================
@login_required
@user_passes_test(is_student)
def student_applications(request):
    applications = ScholarshipApplication.objects.filter(student=request.user)
    return render(request, 'applications/student_applications.html', {'applications': applications})


# =========================
# Teacher/Admin: Review applications
# =========================
@login_required
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

