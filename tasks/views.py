from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.contrib.auth.views import LoginView
from django.contrib import messages


def home(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(completed=True).count()
        active_tasks = tasks.filter(completed=False).count()

        return render(request, 'tasks/home.html', {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'active_tasks': active_tasks
        })

    return render(request, 'tasks/home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Automatically log in the user after registration
            login(request, user)

            return redirect('task-list')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/signup.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title:
            Task.objects.create(user=request.user, title=title, description=description)
            messages.success(request, 'Task added successfully!')
            return redirect('task-list')
        else:
            messages.error(request, 'Title is required!')
        
    return render(request, 'tasks/add_task.html')


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.completed = True
        task.save()
        messages.success(request, 'Well done!')
    return redirect('task-list')


@login_required
def uncomplete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.completed = False
        task.save()
    return redirect('task-list')


@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.user == request.user:
        task.delete()
        messages.success(request, 'Task deleted!')
    return redirect('task-list')


class CustomLoginView(LoginView):
    template_name = 'tasks/login.html'

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        
        # Set session expiry based on the "remember me" checkbox
        if not remember_me:
            self.request.session.set_expiry(0)  # Session expires when the browser is closed
        else:
            self.request.session.set_expiry(1209600)  # 2 weeks
        
        return super().form_valid(form)
