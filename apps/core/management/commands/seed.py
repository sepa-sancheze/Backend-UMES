import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.academics.models import Department, Faculty, Program
from apps.classes.models import ClassSection, Schedule, Subject
from apps.enrollments.models import Enrollment, Grade
from apps.staff.models import Teacher
from apps.students.models import Student


# ---------------------------------------------------------------------------
# Static data pools
# ---------------------------------------------------------------------------

FACULTIES = [
    {'name': 'Faculty of Engineering', 'code': 'ENG', 'dean_name': 'Dr. Robert Hughes'},
    {'name': 'Faculty of Business', 'code': 'BUS', 'dean_name': 'Dr. Sandra Mills'},
    {'name': 'Faculty of Sciences', 'code': 'SCI', 'dean_name': 'Dr. Carlos Vega'},
]

DEPARTMENTS = [
    # Engineering
    {'faculty_code': 'ENG', 'name': 'Software Engineering', 'code': 'SE', 'head_name': 'Dr. Alan Park'},
    {'faculty_code': 'ENG', 'name': 'Civil Engineering', 'code': 'CE', 'head_name': 'Dr. Maria Torres'},
    {'faculty_code': 'ENG', 'name': 'Electrical Engineering', 'code': 'EE', 'head_name': 'Dr. James Lin'},
    # Business
    {'faculty_code': 'BUS', 'name': 'Accounting', 'code': 'ACC', 'head_name': 'Dr. Laura Gomez'},
    {'faculty_code': 'BUS', 'name': 'Marketing', 'code': 'MKT', 'head_name': 'Dr. Tom Fisher'},
    {'faculty_code': 'BUS', 'name': 'Management', 'code': 'MGT', 'head_name': 'Dr. Anne Clarke'},
    # Sciences
    {'faculty_code': 'SCI', 'name': 'Mathematics', 'code': 'MAT', 'head_name': 'Dr. Nina Reyes'},
    {'faculty_code': 'SCI', 'name': 'Physics', 'code': 'PHY', 'head_name': 'Dr. Paul Novak'},
    {'faculty_code': 'SCI', 'name': 'Biology', 'code': 'BIO', 'head_name': 'Dr. Eva Solis'},
]

PROGRAMS = [
    {'dept_code': 'SE', 'name': 'Computer Science', 'code': 'CS', 'level': 'undergraduate', 'semesters': 8, 'credits': 160},
    {'dept_code': 'SE', 'name': 'Software Engineering', 'code': 'SWE', 'level': 'undergraduate', 'semesters': 8, 'credits': 168},
    {'dept_code': 'CE', 'name': 'Civil Engineering', 'code': 'CIVE', 'level': 'undergraduate', 'semesters': 10, 'credits': 200},
    {'dept_code': 'EE', 'name': 'Electrical Engineering', 'code': 'ELEE', 'level': 'undergraduate', 'semesters': 8, 'credits': 165},
    {'dept_code': 'ACC', 'name': 'Accounting', 'code': 'ACCT', 'level': 'undergraduate', 'semesters': 8, 'credits': 155},
    {'dept_code': 'MKT', 'name': 'Marketing', 'code': 'MRKT', 'level': 'undergraduate', 'semesters': 8, 'credits': 150},
    {'dept_code': 'MGT', 'name': 'Business Administration', 'code': 'BA', 'level': 'undergraduate', 'semesters': 8, 'credits': 155},
    {'dept_code': 'MGT', 'name': 'Master of Business Administration', 'code': 'MBA', 'level': 'graduate', 'semesters': 4, 'credits': 60},
    {'dept_code': 'MAT', 'name': 'Applied Mathematics', 'code': 'AMAT', 'level': 'undergraduate', 'semesters': 8, 'credits': 160},
    {'dept_code': 'PHY', 'name': 'Physics', 'code': 'PHYS', 'level': 'undergraduate', 'semesters': 8, 'credits': 158},
    {'dept_code': 'BIO', 'name': 'Biology', 'code': 'BIOL', 'level': 'undergraduate', 'semesters': 8, 'credits': 155},
]

# Subjects per program (code_prefix, name, credits, semester, mandatory)
SUBJECTS_BY_PROGRAM = {
    'CS': [
        ('CS101', 'Introduction to Programming', 4, 1, True),
        ('CS102', 'Data Structures', 4, 2, True),
        ('CS201', 'Algorithms', 3, 3, True),
        ('CS202', 'Operating Systems', 3, 3, True),
        ('CS301', 'Database Systems', 3, 4, True),
        ('CS302', 'Computer Networks', 3, 4, True),
        ('CS401', 'Software Architecture', 3, 5, True),
        ('CS402', 'Artificial Intelligence', 3, 6, False),
    ],
    'SWE': [
        ('SWE101', 'Programming Fundamentals', 4, 1, True),
        ('SWE102', 'Object-Oriented Design', 3, 2, True),
        ('SWE201', 'Software Requirements', 3, 3, True),
        ('SWE202', 'Agile Development', 3, 3, True),
        ('SWE301', 'Testing and QA', 3, 4, True),
        ('SWE302', 'DevOps Practices', 3, 5, False),
        ('SWE401', 'Capstone Project', 6, 7, True),
    ],
    'CIVE': [
        ('CE101', 'Engineering Mechanics', 4, 1, True),
        ('CE102', 'Engineering Drawing', 3, 1, True),
        ('CE201', 'Structural Analysis', 4, 3, True),
        ('CE202', 'Fluid Mechanics', 3, 3, True),
        ('CE301', 'Soil Mechanics', 3, 5, True),
        ('CE401', 'Construction Management', 3, 7, True),
    ],
    'ELEE': [
        ('EE101', 'Circuit Analysis', 4, 1, True),
        ('EE102', 'Electronics I', 3, 2, True),
        ('EE201', 'Signals and Systems', 4, 3, True),
        ('EE202', 'Power Systems', 3, 4, True),
        ('EE301', 'Control Systems', 3, 5, True),
        ('EE401', 'Embedded Systems', 3, 6, False),
    ],
    'ACCT': [
        ('ACC101', 'Financial Accounting', 4, 1, True),
        ('ACC102', 'Managerial Accounting', 3, 2, True),
        ('ACC201', 'Intermediate Accounting', 4, 3, True),
        ('ACC202', 'Cost Accounting', 3, 4, True),
        ('ACC301', 'Auditing', 3, 5, True),
        ('ACC401', 'Tax Accounting', 3, 6, True),
    ],
    'MRKT': [
        ('MKT101', 'Principles of Marketing', 3, 1, True),
        ('MKT102', 'Consumer Behavior', 3, 2, True),
        ('MKT201', 'Market Research', 3, 3, True),
        ('MKT202', 'Digital Marketing', 3, 4, False),
        ('MKT301', 'Brand Management', 3, 5, True),
        ('MKT401', 'Marketing Strategy', 3, 7, True),
    ],
    'BA': [
        ('BA101', 'Principles of Management', 3, 1, True),
        ('BA102', 'Business Communication', 3, 1, True),
        ('BA201', 'Organizational Behavior', 3, 3, True),
        ('BA202', 'Operations Management', 3, 4, True),
        ('BA301', 'Strategic Management', 3, 5, True),
        ('BA401', 'Entrepreneurship', 3, 7, False),
    ],
    'MBA': [
        ('MBA101', 'Business Strategy', 3, 1, True),
        ('MBA102', 'Financial Management', 3, 1, True),
        ('MBA201', 'Leadership and Organizations', 3, 2, True),
        ('MBA202', 'Innovation Management', 3, 2, True),
    ],
    'AMAT': [
        ('MAT101', 'Calculus I', 4, 1, True),
        ('MAT102', 'Calculus II', 4, 2, True),
        ('MAT201', 'Linear Algebra', 4, 3, True),
        ('MAT202', 'Differential Equations', 4, 3, True),
        ('MAT301', 'Numerical Methods', 3, 5, True),
        ('MAT401', 'Mathematical Modeling', 3, 6, True),
    ],
    'PHYS': [
        ('PHY101', 'Classical Mechanics', 4, 1, True),
        ('PHY102', 'Electromagnetism', 4, 2, True),
        ('PHY201', 'Thermodynamics', 3, 3, True),
        ('PHY202', 'Quantum Mechanics', 4, 4, True),
        ('PHY301', 'Optics', 3, 5, False),
        ('PHY401', 'Nuclear Physics', 3, 6, False),
    ],
    'BIOL': [
        ('BIO101', 'Cell Biology', 4, 1, True),
        ('BIO102', 'Genetics', 3, 2, True),
        ('BIO201', 'Microbiology', 3, 3, True),
        ('BIO202', 'Ecology', 3, 4, True),
        ('BIO301', 'Biochemistry', 4, 5, True),
        ('BIO401', 'Molecular Biology', 4, 6, True),
    ],
}

FIRST_NAMES = [
    'James', 'Maria', 'Carlos', 'Sofia', 'David', 'Laura', 'Michael',
    'Isabella', 'Daniel', 'Emma', 'Luis', 'Valeria', 'Kevin', 'Camila',
    'Robert', 'Natalia', 'Steven', 'Andres', 'Patricia', 'Diego',
    'Ana', 'Jorge', 'Sandra', 'Felipe', 'Monica', 'Alejandro', 'Clara',
    'Ricardo', 'Paola', 'Sebastian',
]

LAST_NAMES = [
    'Garcia', 'Rodriguez', 'Martinez', 'Lopez', 'Hernandez', 'Gonzalez',
    'Perez', 'Sanchez', 'Ramirez', 'Torres', 'Flores', 'Rivera', 'Gomez',
    'Diaz', 'Cruz', 'Morales', 'Reyes', 'Gutierrez', 'Ortiz', 'Vargas',
    'Castillo', 'Romero', 'Alvarez', 'Moreno', 'Jimenez', 'Ruiz', 'Silva',
    'Mendoza', 'Aguilar', 'Vega',
]

SPECIALIZATIONS = [
    'Algorithms and Complexity', 'Machine Learning', 'Computer Vision',
    'Distributed Systems', 'Cybersecurity', 'Cloud Computing',
    'Financial Analysis', 'Econometrics', 'Supply Chain Management',
    'Structural Dynamics', 'Renewable Energy', 'Signal Processing',
    'Applied Statistics', 'Quantum Computing', 'Molecular Genetics',
    'Environmental Science', 'Strategic Planning', 'Digital Transformation',
]

ACADEMIC_DEGREES = ['B.Sc.', 'M.Sc.', 'Ph.D.', 'M.B.A.', 'M.Eng.']

CLASSROOMS = [
    'A-101', 'A-102', 'A-201', 'A-202', 'B-101', 'B-102', 'B-201',
    'C-301', 'C-302', 'Lab-1', 'Lab-2', 'Auditorium', 'Online',
]


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _random_date(start_year: int, end_year: int) -> date:
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))


def _unique_email(first: str, last: str, domain: str, existing: set) -> str:
    base = f'{first.lower()}.{last.lower()}'
    email = f'{base}@{domain}'
    counter = 1
    while email in existing:
        email = f'{base}{counter}@{domain}'
        counter += 1
    existing.add(email)
    return email


def _pick(pool: list):
    return random.choice(pool)


# ---------------------------------------------------------------------------
# Command
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = 'Seed the database with dummy university data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete all existing records before seeding.',
        )
        parser.add_argument(
            '--students',
            type=int,
            default=8,
            help='Number of students to create per program (default: 8).',
        )
        parser.add_argument(
            '--teachers',
            type=int,
            default=3,
            help='Number of teachers to create per department (default: 3).',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['flush']:
            self.stdout.write(self.style.WARNING('Flushing existing data...'))
            Grade.objects.all().delete()
            Enrollment.objects.all().delete()
            Schedule.objects.all().delete()
            ClassSection.objects.all().delete()
            Subject.objects.all().delete()
            Student.objects.all().delete()
            Teacher.objects.all().delete()
            Program.objects.all().delete()
            Department.objects.all().delete()
            Faculty.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Flush complete.\n'))

        students_per_program = options['students']
        teachers_per_dept = options['teachers']

        self._seed_faculties()
        self._seed_departments()
        self._seed_programs()
        self._seed_teachers(teachers_per_dept)
        self._seed_subjects()
        self._seed_sections_and_schedules()
        self._seed_students(students_per_program)
        self._seed_enrollments_and_grades()

        self.stdout.write(self.style.SUCCESS('\nSeeding complete!'))
        self._print_summary()

    # ------------------------------------------------------------------
    # Seeders
    # ------------------------------------------------------------------

    def _seed_faculties(self):
        created = 0
        for data in FACULTIES:
            _, new = Faculty.objects.get_or_create(
                code=data['code'],
                defaults={
                    'name': data['name'],
                    'dean_name': data['dean_name'],
                    'description': f'The {data["name"]} provides world-class education.',
                },
            )
            if new:
                created += 1
        self.stdout.write(f'  Faculties   : {created} created ({Faculty.objects.count()} total)')

    def _seed_departments(self):
        created = 0
        faculty_map = {f.code: f for f in Faculty.objects.all()}
        for data in DEPARTMENTS:
            faculty = faculty_map.get(data['faculty_code'])
            if not faculty:
                continue
            _, new = Department.objects.get_or_create(
                code=data['code'],
                defaults={
                    'faculty': faculty,
                    'name': data['name'],
                    'head_name': data['head_name'],
                    'description': f'Department of {data["name"]}.',
                },
            )
            if new:
                created += 1
        self.stdout.write(f'  Departments : {created} created ({Department.objects.count()} total)')

    def _seed_programs(self):
        created = 0
        dept_map = {d.code: d for d in Department.objects.all()}
        for data in PROGRAMS:
            dept = dept_map.get(data['dept_code'])
            if not dept:
                continue
            _, new = Program.objects.get_or_create(
                code=data['code'],
                defaults={
                    'department': dept,
                    'name': data['name'],
                    'level': data['level'],
                    'duration_semesters': data['semesters'],
                    'total_credits': data['credits'],
                    'description': f'{data["name"]} program — {data["level"]} level.',
                    'is_active': True,
                },
            )
            if new:
                created += 1
        self.stdout.write(f'  Programs    : {created} created ({Program.objects.count()} total)')

    def _seed_teachers(self, per_dept: int):
        existing_emails: set = set(Teacher.objects.values_list('email', flat=True))
        existing_ids: set = set(Teacher.objects.values_list('employee_id', flat=True))
        created = 0
        emp_counter = Teacher.objects.count() + 1

        for dept in Department.objects.all():
            current_count = dept.teachers.filter(is_deleted=False).count()
            needed = max(0, per_dept - current_count)
            for _ in range(needed):
                first = _pick(FIRST_NAMES)
                last = _pick(LAST_NAMES)
                email = _unique_email(first, last, 'umes.edu', existing_emails)

                emp_id = f'T{emp_counter:04d}'
                while emp_id in existing_ids:
                    emp_counter += 1
                    emp_id = f'T{emp_counter:04d}'
                existing_ids.add(emp_id)

                Teacher.objects.create(
                    department=dept,
                    employee_id=emp_id,
                    first_name=first,
                    last_name=last,
                    email=email,
                    phone=f'+1-555-{random.randint(1000, 9999)}',
                    specialization=_pick(SPECIALIZATIONS),
                    academic_degree=_pick(ACADEMIC_DEGREES),
                    contract_type=random.choices(
                        ['full_time', 'part_time', 'visiting'], weights=[60, 25, 15]
                    )[0],
                    hire_date=_random_date(2010, 2024),
                    is_active=True,
                )
                emp_counter += 1
                created += 1

        self.stdout.write(f'  Teachers    : {created} created ({Teacher.objects.count()} total)')

    def _seed_subjects(self):
        created = 0
        program_map = {p.code: p for p in Program.objects.all()}
        for prog_code, subjects in SUBJECTS_BY_PROGRAM.items():
            program = program_map.get(prog_code)
            if not program:
                continue
            for (code, name, credits, semester, mandatory) in subjects:
                _, new = Subject.objects.get_or_create(
                    code=code,
                    defaults={
                        'program': program,
                        'name': name,
                        'credits': credits,
                        'semester': semester,
                        'is_mandatory': mandatory,
                        'description': f'{name} — core subject for {program.name}.',
                    },
                )
                if new:
                    created += 1
        self.stdout.write(f'  Subjects    : {created} created ({Subject.objects.count()} total)')

    def _seed_sections_and_schedules(self):
        sections_created = 0
        schedules_created = 0
        academic_year = 2025
        semester = 1

        day_pairs = [(0, 2), (1, 3), (0, 2, 4), (1, 3)]  # Mon/Wed, Tue/Thu, MWF, Tue/Thu
        time_slots = [
            ('07:00', '08:30'),
            ('08:30', '10:00'),
            ('10:00', '11:30'),
            ('11:30', '13:00'),
            ('14:00', '15:30'),
            ('15:30', '17:00'),
        ]

        for subject in Subject.objects.select_related('program__department').all():
            dept = subject.program.department
            teachers = list(dept.teachers.filter(is_deleted=False, is_active=True))
            if not teachers:
                teachers = list(Teacher.objects.filter(is_active=True, is_deleted=False)[:1])
            if not teachers:
                continue

            section_code = 'A'
            existing = ClassSection.objects.filter(
                subject=subject, section_code=section_code,
                academic_year=academic_year, semester=semester,
            ).exists()
            if not existing:
                section = ClassSection.objects.create(
                    subject=subject,
                    teacher=_pick(teachers),
                    section_code=section_code,
                    academic_year=academic_year,
                    semester=semester,
                    period=random.choice(['morning', 'afternoon', 'evening']),
                    classroom=_pick(CLASSROOMS),
                    max_capacity=random.randint(25, 40),
                    is_open=True,
                )
                sections_created += 1

                days = _pick(day_pairs)
                start_str, end_str = _pick(time_slots)
                from datetime import time as dtime

                def _t(ts):
                    h, m = map(int, ts.split(':'))
                    return dtime(h, m)

                for day in days:
                    if not Schedule.objects.filter(section=section, day_of_week=day).exists():
                        Schedule.objects.create(
                            section=section,
                            day_of_week=day,
                            start_time=_t(start_str),
                            end_time=_t(end_str),
                        )
                        schedules_created += 1

        self.stdout.write(
            f'  Sections    : {sections_created} created ({ClassSection.objects.count()} total)'
        )
        self.stdout.write(
            f'  Schedules   : {schedules_created} created ({Schedule.objects.count()} total)'
        )

    def _seed_students(self, per_program: int):
        existing_emails: set = set(Student.objects.values_list('email', flat=True))
        existing_ids: set = set(Student.objects.values_list('student_id', flat=True))
        created = 0
        stu_counter = Student.objects.count() + 1

        for program in Program.objects.all():
            current_count = program.students.filter(is_deleted=False).count()
            needed = max(0, per_program - current_count)
            for _ in range(needed):
                first = _pick(FIRST_NAMES)
                last = _pick(LAST_NAMES)
                email = _unique_email(first, last, 'student.umes.edu', existing_emails)

                stu_id = f'S{stu_counter:05d}'
                while stu_id in existing_ids:
                    stu_counter += 1
                    stu_id = f'S{stu_counter:05d}'
                existing_ids.add(stu_id)

                semester = random.randint(1, program.duration_semesters)
                Student.objects.create(
                    program=program,
                    student_id=stu_id,
                    first_name=first,
                    last_name=last,
                    email=email,
                    phone=f'+1-555-{random.randint(1000, 9999)}',
                    date_of_birth=_random_date(1998, 2005),
                    address=f'{random.randint(1, 999)} Main St, City, Country',
                    enrollment_date=_random_date(2022, 2025),
                    current_semester=semester,
                    status=random.choices(
                        ['active', 'active', 'active', 'inactive', 'suspended'],
                        weights=[70, 10, 5, 10, 5],
                    )[0],
                )
                stu_counter += 1
                created += 1

        self.stdout.write(f'  Students    : {created} created ({Student.objects.count()} total)')

    def _seed_enrollments_and_grades(self):
        enrollments_created = 0
        grades_created = 0

        letter_weights = {
            'A': 30, 'B': 35, 'C': 20, 'D': 8, 'F': 5, 'I': 1, 'W': 1
        }
        letter_to_numeric = {
            'A': (85, 100), 'B': (70, 84), 'C': (60, 69),
            'D': (50, 59), 'F': (0, 49), 'I': None, 'W': None,
        }

        active_students = list(
            Student.objects.filter(is_deleted=False, status='active')
            .select_related('program')
        )

        for student in active_students:
            # Enroll in subjects matching the student's current semester (±1)
            target_semesters = [
                max(1, student.current_semester - 1),
                student.current_semester,
            ]
            candidate_sections = list(
                ClassSection.objects.filter(
                    is_deleted=False,
                    is_open=True,
                    subject__program=student.program,
                    subject__semester__in=target_semesters,
                ).exclude(
                    enrollments__student=student
                ).select_related('subject')
            )

            random.shuffle(candidate_sections)
            max_enroll = min(5, len(candidate_sections))
            if max_enroll == 0:
                continue
            enroll_in = candidate_sections[:random.randint(1, max_enroll)]

            for section in enroll_in:
                enrollment = Enrollment.objects.create(
                    student=student,
                    section=section,
                    status='enrolled',
                )
                enrollments_created += 1

                # Grade past-semester subjects
                if section.subject.semester < student.current_semester:
                    letter = random.choices(
                        list(letter_weights.keys()),
                        weights=list(letter_weights.values()),
                    )[0]
                    numeric_range = letter_to_numeric[letter]
                    numeric = (
                        round(random.uniform(*numeric_range), 2)
                        if numeric_range else None
                    )
                    Grade.objects.create(
                        enrollment=enrollment,
                        letter_grade=letter,
                        numeric_grade=numeric,
                        graded_at=timezone.now() - timedelta(days=random.randint(30, 180)),
                        graded_by=section.teacher,
                    )
                    enrollment.status = 'completed' if letter not in ('F', 'W') else 'failed'
                    enrollment.save(update_fields=['status', 'updated_at'])
                    grades_created += 1

        self.stdout.write(
            f'  Enrollments : {enrollments_created} created ({Enrollment.objects.count()} total)'
        )
        self.stdout.write(
            f'  Grades      : {grades_created} created ({Grade.objects.count()} total)'
        )

    def _print_summary(self):
        self.stdout.write('\n' + '=' * 45)
        self.stdout.write(self.style.SUCCESS('  Database summary'))
        self.stdout.write('=' * 45)
        rows = [
            ('Faculties', Faculty.objects.count()),
            ('Departments', Department.objects.count()),
            ('Programs', Program.objects.count()),
            ('Teachers', Teacher.objects.count()),
            ('Subjects', Subject.objects.count()),
            ('Class Sections', ClassSection.objects.count()),
            ('Schedules', Schedule.objects.count()),
            ('Students', Student.objects.count()),
            ('Enrollments', Enrollment.objects.count()),
            ('Grades', Grade.objects.count()),
        ]
        for label, count in rows:
            self.stdout.write(f'  {label:<20} {count:>5}')
        self.stdout.write('=' * 45)
