from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('links/', views.links, name='links'),
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/delete/<int:pk>/', views.delete_announcement, name='delete_announcement'),
    path('notes/', views.notes, name='notes'),
    path('notes/delete/<int:pk>/', views.delete_note, name='delete_note'),
    path('assignments/', views.assignments, name='assignments'),
    path('assignments/delete/<int:pk>/', views.delete_assignment, name='delete_assignment'),
    path('upload-notes/', views.upload_notes, name='upload_notes'),
    path('upload-assignments/', views.upload_assignments, name='upload_assignments'),
    path('write-announcements/', views.write_announcements, name='write_announcements'),
    path('timetable/', views.timetable, name='timetable'),
    path('reminder/', views.reminder, name='reminder'),
]