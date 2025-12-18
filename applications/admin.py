from django.contrib import admin
from .models import ScholarshipApplication, Renewal

# Register your models here.
admin.site.register(ScholarshipApplication)
admin.site.register(Renewal)
