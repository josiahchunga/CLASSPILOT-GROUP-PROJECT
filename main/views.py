import json
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import RegisterForm, AnnouncementForm, NoteForm, AssignmentForm
from .models import Announcement, Note, Assignment

REDIRECT_BY_ROLE = {
    'student': '/links/',
    'lecture': '/upload-notes/',
    'classrep/student': '/write-announcements/',
}


def _is_json_request(request):
    content_type = request.headers.get('Content-Type', '') or request.content_type or ''
    return request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in content_type.lower()


@csrf_exempt
def register(request):
    if request.method == 'POST':
        is_json_request = _is_json_request(request)
        if is_json_request and request.body:
            payload = json.loads(request.body.decode('utf-8'))
            data = payload
        else:
            data = request.POST

        form = RegisterForm(data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            redirect_url = REDIRECT_BY_ROLE.get(user.role, '/links/')
            if is_json_request:
                return JsonResponse({'redirect_url': redirect_url})
            return redirect(redirect_url)
        if is_json_request:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = RegisterForm()
    return render(request, 'main/create_account.html', {'form': form})


@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect('links')

    is_json_request = _is_json_request(request)
    if request.method == 'POST':
        if is_json_request and request.body:
            try:
                payload = json.loads(request.body.decode('utf-8'))
            except (TypeError, ValueError):
                return JsonResponse({'errors': {'non_field_errors': ['Invalid JSON payload']}}, status=400)
            form = AuthenticationForm(request, data=payload)
        else:
            form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if is_json_request:
                return JsonResponse({'redirect_url': '/links/'})
            return redirect('links')
        if is_json_request:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def links(request):
    return render(request, 'main/links.html')


@login_required
def announcements(request):
    items = Announcement.objects.order_by('-created_at')
    return render(request, 'main/announcements.html', {'items': items})


@login_required
def notes(request):
    items = Note.objects.order_by('-created_at')
    return render(request, 'main/notes.html', {'items': items})


@login_required
def assignments(request):
    items = Assignment.objects.order_by('-created_at')
    return render(request, 'main/assignments.html', {'items': items})


@login_required
def upload_notes(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            return redirect('notes')
    else:
        form = NoteForm()
    return render(request, 'main/upload_notes.html', {'form': form})


@login_required
def upload_assignments(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.author = request.user
            assignment.save()
            return redirect('assignments')
    else:
        form = AssignmentForm()
    return render(request, 'main/upload_assignments.html', {'form': form})


@login_required
def write_announcements(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            return redirect('announcements')
    else:
        form = AnnouncementForm()
    return render(request, 'main/write_announcements.html', {'form': form})


@login_required
@require_POST
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if announcement.author_id != request.user.id:
        return redirect('announcements')
    announcement.delete()
    return redirect('announcements')


@login_required
@require_POST
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if note.author_id != request.user.id:
        return redirect('notes')
    note.delete()
    return redirect('notes')


@login_required
@require_POST
def delete_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if assignment.author_id != request.user.id:
        return redirect('assignments')
    assignment.delete()
    return redirect('assignments')


@login_required
def timetable(request):
    return render(request, 'main/timetable.html')


@login_required
def reminder(request):
    return render(request, 'main/reminder.html')
