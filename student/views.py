from django.shortcuts import render, redirect
from .models import student_data

# Create your views here.
def student_index(request):
    return render(request, 'student_index.html')

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
        return redirect('student_register_success')

    return render(request, 'student_signIn.html')

def student_register_success(request):
    return render(request, 'student_register_success.html')
