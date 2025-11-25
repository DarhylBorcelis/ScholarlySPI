from django.shortcuts import render, redirect
from .models import student_data

# Create your views here.
def student_index(request):
    return render(request, 'student_html/student_index.html')

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

    return render(request, 'student_html/student_signIn.html')

def student_logIn(request):
    message = ''
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student_email = request.POST.get('student_email')
        student_pass = request.POST.get('student_password')
    
        try:
            student = student_data.objects.get(student_id=student_id, student_email=student_email)
            
            if student.student_password != student_pass:
                message = "Incorrect password"
            else:
                # Store student info in session
                request.session['student_id'] = student.student_id
                request.session['student_name'] = student.student_fullname
                return redirect('student_dashboard')

        except student_data.DoesNotExist:
            message = "Invalid Student ID or Email"

    return render(request, 'student_html/student_logIn.html', {'message': message})

def student_register_success(request):
    return render(request, 'student_html/student_register_success.html')

def student_dashboard(request):
    if 'student_id' not in request.session:
        return redirect('student_logIn')

    student_name = request.session.get('student_name')
    return render(request, 'student_html/student_dashboard.html', {'student_name': student_name})

def student_logout(request):
    request.session.flush()    # Clear the session
    return redirect('student_logIn')
