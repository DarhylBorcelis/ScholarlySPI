from django.contrib import admin
from .models import student_data


class student_data_Admin(admin.ModelAdmin):
    list_display = ('student_id', 
                    'student_fullname', 
                    'student_contact', 
                    'student_email', 
                    'student_grade', 
                    'student_course',
                    'student_password'
                    )


    



# Register your models here.
admin.site.register(student_data, student_data_Admin)