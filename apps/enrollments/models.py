from django.db import models
from apps.core.models import BaseModel


class Enrollment(BaseModel):
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    student = models.ForeignKey(
        'students.Student', on_delete=models.PROTECT, related_name='enrollments'
    )
    section = models.ForeignKey(
        'classes.ClassSection', on_delete=models.PROTECT, related_name='enrollments'
    )
    enrolled_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
        unique_together = ('student', 'section')
        ordering = ['-enrolled_date']

    def __str__(self):
        return f'{self.student} → {self.section}'


class Grade(BaseModel):
    LETTER_CHOICES = [
        ('A', 'A - Excellent'),
        ('B', 'B - Good'),
        ('C', 'C - Satisfactory'),
        ('D', 'D - Passing'),
        ('F', 'F - Failing'),
        ('I', 'I - Incomplete'),
        ('W', 'W - Withdrawn'),
    ]

    enrollment = models.OneToOneField(
        Enrollment, on_delete=models.PROTECT, related_name='grade'
    )
    numeric_grade = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    letter_grade = models.CharField(
        max_length=2, choices=LETTER_CHOICES, null=True, blank=True
    )
    graded_at = models.DateTimeField(null=True, blank=True)
    graded_by = models.ForeignKey(
        'staff.Teacher', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='graded_grades'
    )
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
        ordering = ['-graded_at']

    def __str__(self):
        return f"{self.enrollment} — {self.letter_grade or self.numeric_grade or 'Pending'}"
