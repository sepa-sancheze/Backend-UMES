from django.db import models
from apps.core.models import BaseModel


class Faculty(BaseModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    dean_name = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'
        ordering = ['name']

    def __str__(self):
        return f'{self.code} - {self.name}'


class Department(BaseModel):
    faculty = models.ForeignKey(
        Faculty, on_delete=models.PROTECT, related_name='departments'
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    head_name = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['faculty__name', 'name']

    def __str__(self):
        return f'{self.code} - {self.name}'


class Program(BaseModel):
    LEVEL_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('doctorate', 'Doctorate'),
        ('technical', 'Technical'),
    ]

    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name='programs'
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='undergraduate')
    duration_semesters = models.PositiveSmallIntegerField(default=8)
    total_credits = models.PositiveSmallIntegerField(default=160)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'
        ordering = ['department__name', 'name']

    def __str__(self):
        return f'{self.code} - {self.name}'
