from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from main.models import Announcement, Note, Assignment

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample data for ClassPilot'

    def handle(self, *args, **options):
        # Create sample users
        if not User.objects.filter(username='student1').exists():
            student = User.objects.create_user(
                username='student1',
                email='student1@classpilot.com',
                password='password123',
                role='student',
                phone_number='0999-11-22-33'
            )
            self.stdout.write(f'Created student: {student.username}')

        if not User.objects.filter(username='lecturer1').exists():
            lecturer = User.objects.create_user(
                username='lecturer1',
                email='lecturer1@classpilot.com',
                password='password123',
                role='lecture',
                phone_number='0999-44-55-66'
            )
            self.stdout.write(f'Created lecturer: {lecturer.username}')

        if not User.objects.filter(username='classrep1').exists():
            classrep = User.objects.create_user(
                username='classrep1',
                email='classrep1@classpilot.com',
                password='password123',
                role='classrep/student',
                phone_number='0999-77-88-99'
            )
            self.stdout.write(f'Created class rep: {classrep.username}')

        # Create sample announcements
        if not Announcement.objects.filter(title='Welcome to ClassPilot').exists():
            Announcement.objects.create(
                title='Welcome to ClassPilot',
                message='Welcome to our new classroom management system! This platform will help us collaborate better on assignments, notes, and announcements.',
                author=classrep
            )
            self.stdout.write('Created sample announcement')

        # Create sample notes
        if not Note.objects.filter(title='Data Science Fundamentals').exists():
            Note.objects.create(
                title='Data Science Fundamentals',
                description='Introduction to data science concepts including statistics, machine learning, and data visualization.',
                author=lecturer,
                download_url='https://example.com/data_science_notes.pdf'
            )
            self.stdout.write('Created sample note')

        # Create sample assignments
        if not Assignment.objects.filter(title='Data Analysis Project').exists():
            Assignment.objects.create(
                title='Data Analysis Project',
                description='Analyze the provided dataset and create visualizations. Submit your findings and code by the deadline.',
                author=lecturer,
                download_url='https://example.com/data_analysis_assignment.pdf'
            )
            self.stdout.write('Created sample assignment')

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with sample data!'))
