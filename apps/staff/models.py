from django.db import models
from apps.core.models import BaseModel


class Teacher(BaseModel):
    CONTRACT_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('visiting', 'Visiting'),
    ]

    department = models.ForeignKey(
        'academics.Department', on_delete=models.PROTECT, related_name='teachers'
    )
    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    academic_degree = models.CharField(max_length=100, blank=True)
    contract_type = models.CharField(max_length=20, choices=CONTRACT_CHOICES, default='full_time')
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.employee_id} - {self.last_name}, {self.first_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
