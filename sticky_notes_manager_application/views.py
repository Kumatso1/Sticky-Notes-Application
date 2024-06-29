from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, NoteForm
from .models import Note, User

def is_admin(user):
    return user.is_admin

def register(request):
    if User.objects.filter(is_admin=True).exists() and not request.user.is_admin:
        messages.error(request, 'Admin account already exists.')
        return redirect('login')
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if not User.objects.filter(is_admin=True).exists():
                user.is_admin = True
            user.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'notes/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'notes/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.is_admin:
        users = User.objects.all()
        notes = Note.objects.all()
        return render(request, 'notes/admin_dashboard.html', {'users': users, 'notes': notes})
    else:
        notes = Note.objects.filter(created_by=request.user)
        return render(request, 'notes/user_dashboard.html', {'notes': notes})

@login_required
@user_passes_test(is_admin)
def create_admin(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = True
            user.save()
            messages.success(request, f'Admin account created for {user.username}!')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'notes/create_admin.html', {'form': form})

@login_required
def note_list(request):
    if request.user.is_admin:
        notes = Note.objects.all()
    else:
        notes = Note.objects.filter(created_by=request.user)
    return render(request, 'notes/note_list.html', {'notes': notes})

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})

@login_required
def note_new(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.created_by = request.user
            note.save()
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm()
    return render(request, 'notes/note_edit.html', {'form': form})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_edit.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    note.delete()
    return redirect('note_list')


# Create your views here.
