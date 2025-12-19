from django.contrib import admin
from .models import ScholarshipApplication, StudentProfile, Renewal



# Register your models here.
admin.site.register(StudentProfile)
admin.site.register(ScholarshipApplication)
admin.site.register(Renewal)

