from django.db import models
from django.contrib.auth.models import User

# Student Profile Model
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100, null=True, blank=True)
    year_level = models.IntegerField(null=True, blank=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    profile_image = models.FileField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.student_id
    

def scholarship_upload_path(instance, filename, doc_type='other'): return f"scholarship_docs/{instance.student.username}/{doc_type}/{filename}" 
def birth_certificate_upload(instance, filename): return scholarship_upload_path(instance, filename, 'birth_certificate') 
def report_card_upload(instance, filename): return scholarship_upload_path(instance, filename, 'report_card')
def enrollment_cert_upload(instance, filename): return scholarship_upload_path(instance, filename, 'enrollment_cert') 
def good_moral_upload(instance, filename): return scholarship_upload_path(instance, filename, 'good_moral') 
def id_photo_upload(instance, filename): return scholarship_upload_path(instance, filename, 'id_photo')
def proof_identity_upload(instance, filename):
    return scholarship_upload_path(instance, filename, 'proof_identity')
def transcript_records_upload(instance, filename):
    return scholarship_upload_path(instance, filename, 'transcript_records')
def scholarship_essay_upload(instance, filename):
    return scholarship_upload_path(instance, filename, 'scholarship_essay')

SEMESTER_CHOICES = [
    ('1st', '1st Semester'),
    ('2nd', '2nd Semester'),
    ('3rd', '3rd Semester'),
    ('4th', '4th Semester'),
]

SEX_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
]

# ----------- Scholarship Application Model -----------
class ScholarshipApplication(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    # Student Info
    previous_school = models.CharField(max_length=100)
    school_year = models.CharField(max_length=20)
    surname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    age = models.PositiveIntegerField()
    street_no = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    cellphone = models.CharField(max_length=11)
    semester = models.CharField(max_length=5, choices=SEMESTER_CHOICES)
    strand_course = models.CharField(max_length=100)
    application_date = models.DateField()

    # Documents
    proof_identity = models.FileField(upload_to=proof_identity_upload, null=True, blank=True)
    birth_certificate = models.FileField(upload_to=birth_certificate_upload, null=True, blank=True)
    transcript_records = models.FileField(upload_to=transcript_records_upload, null=True, blank=True)
    enrollment_certificate = models.FileField(upload_to=enrollment_cert_upload, null=True, blank=True)
    good_moral = models.FileField(upload_to=good_moral_upload, null=True, blank=True)
    scholarship_essay = models.FileField(upload_to=scholarship_essay_upload, null=True, blank=True)

    # Status & Timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.surname}, {self.firstname} - {self.status}"

    
def renew_scholarship_upload_path(instance, filename, doc_type='other'):
    return f"renewal_docs/{instance.student.username}/{doc_type}/{filename}"
def renew_birth_certificate_upload(instance, filename):
    return renew_scholarship_upload_path(instance, filename, 'birth_certificate')
def renew_report_card_upload(instance, filename):
    return renew_scholarship_upload_path(instance, filename, 'report_card')
def renew_enrollment_cert_upload(instance, filename):
    return renew_scholarship_upload_path(instance, filename, 'enrollment_cert')
def renew_good_moral_upload(instance, filename):
    return renew_scholarship_upload_path(instance, filename, 'good_moral')
def renew_id_photo_upload(instance, filename):
    return renew_scholarship_upload_path(instance, filename, 'id_photo')

class Renewal(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    scholarship = models.ForeignKey(
        'ScholarshipApplication',
        on_delete=models.CASCADE,
        related_name='renewals'
    )
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES, default='1')

    birth_certificate = models.FileField(upload_to=renew_birth_certificate_upload, null=True, blank=True)
    report_card = models.FileField(upload_to=renew_report_card_upload, null=True, blank =True)
    enrollment_cert = models.FileField(upload_to=renew_enrollment_cert_upload, null=True, blank=True)
    good_moral = models.FileField(upload_to=renew_good_moral_upload, null=True, blank=True)
    id_photo = models.FileField(upload_to=renew_id_photo_upload, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'scholarship', 'semester')

    def __str__(self):
        return f"{self.student.username} - {self.semester} ({self.status})"
    























    