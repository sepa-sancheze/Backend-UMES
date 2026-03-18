from django.db import models
from apps.core.models import BaseModel


class Student(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('suspended', 'Suspended'),
        ('withdrawn', 'Withdrawn'),
    ]

    program = models.ForeignKey(
        'academics.Program', on_delete=models.PROTECT, related_name='students'
    )
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    enrollment_date = models.DateField()
    current_semester = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.student_id} - {self.last_name}, {self.first_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
