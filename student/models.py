from django.db import models

# Create your models here.
from django.db import models

class student_info(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    COURSE_CHOICES = [
        ('BSCS', 'BS Computer Science'),
        ('BSBA-FM', 'BSBA Financial Management'),
        ('BSBA-MM', 'BSBA Marketing Management'),
        ('BEED', 'BS Elementary Education'),
        ('BPEd', 'BS Physical Education'),
        ('BSTM', 'BS Tourism Management'),
        ('BSHM', 'BS Hospitality Management'),

    ]

    YEAR_LEVEL_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
    ]

    student_id = models.IntegerField(null=True, unique=True)
    name = models.CharField(max_length=50, null=True)
    course = models.CharField(max_length=50, choices=COURSE_CHOICES, null=True)
    year_level = models.CharField(max_length=30, choices=YEAR_LEVEL_CHOICES, null=True)
    email = models.EmailField(null=True)

    id_picture = models.FileField(upload_to='id_pictures/', null=True, blank=True)
    report_card = models.FileField(upload_to='report_cards/', null=True, blank=True)
    good_moral = models.FileField(upload_to='good_moral/', null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    date_applied = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.name}"




# class scholarship(models.Model):


#     def __str__(self):
#         return self.name
