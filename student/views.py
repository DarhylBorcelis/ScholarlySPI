from django.shortcuts import render, redirect
from .models import student_data

# Create your views here.
def index(request):
    return render(request, 'index.html')

def student_signIn(request):
    if request.method == "POST":
        
        student_data.objects.create(
            student_id=request.POST.get('student_id'),
            student_fullname=request.POST.get('student_fullname'),
            student_contact=request.POST.get('student_contact'),
            student_email=request.POST.get('student_email'),
            student_grade=request.POST.get('student_grade'),
            student_course=request.POST.get('student_course'),
        )
        return redirect('student_dashboard')

    return render(request, 'student_signIn.html')

def student_dashboard(request):
    return render(request, 'student_dashboard.html')
