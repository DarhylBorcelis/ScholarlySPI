from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
)

class ScholarshipApplication(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    document = models.FileField(upload_to='scholarship_docs/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.status}"

class Renewal(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    scholarship = models.ForeignKey(
        'ScholarshipApplication',
        on_delete=models.CASCADE,
        related_name='renewals'
    )
    semester = models.CharField(max_length=50)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    document = models.FileField(upload_to='renewal_docs/')
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