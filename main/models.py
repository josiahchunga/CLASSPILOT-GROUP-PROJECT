from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [
    ('student', 'Student'),
    ('classrep/student', 'Class Rep / Student'),
    ('lecture', 'Lecturer'),
]

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.username} ({self.role})'

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Note(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    download_url = models.URLField(blank=True, default='https://example.com')

    def __str__(self):
        return self.title

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    download_url = models.URLField(blank=True, default='https://example.com')

    def __str__(self):
        return self.title
