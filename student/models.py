from django.db import models

# Create your models here.
class student_data(models.Model):
    COURSE_CHOICES = [
        ('BSCS', 'BSCS'),
        ('BSAB', 'BSAB'),
        ('BSIT', 'BSIT'),
    ]

    student_id = models.IntegerField(unique=True)
    student_fullname = models.CharField(max_length=55)
    student_contact = models.CharField(max_length=20)
    student_email = models.CharField(max_length=100)
    student_grade = models.IntegerField()
    student_course = models.CharField(max_length=20, choices=COURSE_CHOICES, default='BSCS')
    student_password = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.student_fullname} ({self.student_id})"