from django.db import models
from apps.core.models import BaseModel


class Subject(BaseModel):
    program = models.ForeignKey(
        'academics.Program', on_delete=models.PROTECT, related_name='subjects'
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    credits = models.PositiveSmallIntegerField(default=3)
    semester = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)
    is_mandatory = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ['program__name', 'semester', 'name']

    def __str__(self):
        return f'{self.code} - {self.name}'


class ClassSection(BaseModel):
    PERIOD_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('online', 'Online'),
    ]

    subject = models.ForeignKey(
        Subject, on_delete=models.PROTECT, related_name='sections'
    )
    teacher = models.ForeignKey(
        'staff.Teacher', on_delete=models.PROTECT, related_name='sections'
    )
    section_code = models.CharField(max_length=10)
    academic_year = models.PositiveSmallIntegerField()
    semester = models.PositiveSmallIntegerField()
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='morning')
    classroom = models.CharField(max_length=50, blank=True)
    max_capacity = models.PositiveSmallIntegerField(default=30)
    is_open = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Class Section'
        verbose_name_plural = 'Class Sections'
        unique_together = ('subject', 'section_code', 'academic_year', 'semester')
        ordering = ['-academic_year', 'semester', 'subject__name']

    def __str__(self):
        return f'{self.subject.code}-{self.section_code} ({self.academic_year}-{self.semester})'

    @property
    def enrolled_count(self):
        return self.enrollments.filter(is_deleted=False, status='enrolled').count()


class Schedule(BaseModel):
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    section = models.ForeignKey(
        ClassSection, on_delete=models.CASCADE, related_name='schedules'
    )
    day_of_week = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'
        ordering = ['section', 'day_of_week', 'start_time']

    def __str__(self):
        return (
            f'{self.section} - {self.get_day_of_week_display()} '
            f'{self.start_time:%H:%M}-{self.end_time:%H:%M}'
        )
