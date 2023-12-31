from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from .forms import Task_form
from .models import Task
from django.utils import timezone

# Create your views here.
def home(request):
  return render(request, 'home.html')

def signup(request):
  if request.method == 'GET': 
    return render(request, 'signup.html', {
    'form': UserCreationForm
    })
  else:
    if request.POST['password1'] == request.POST['password2']:
      try:
        user = User.objects.create_user(
          username = request.POST['username'],
          password = request.POST['password1']
        )
        user.save()
        login(request, user)
        return redirect('tasks')
      except IntegrityError:
        return render(request, 'signup.html', {
          'form': UserCreationForm,
          'error': 'User already exists'
        })
    return render(request, 'signup.html', {
          'form': UserCreationForm,
          'error': 'Password does not match'
        })

@login_required
def tasks(request):
  # tasks = Task.objects.all()
  tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True).order_by('-created')
  title = 'Tasks Pending'
  return render(request, 'tasks.html', {
    'tasks': tasks,
    'title': title
  })

@login_required
def tasks_completed(request):
  tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
  title = 'Tasks Completed'
  return render(request, 'tasks.html', {
    'tasks': tasks,
    'title': title
  })

# def task_detail(request, task_id):
#   tasks = Task.objects.filter(id=task_id, user=request.user)
#   error = 'Ohh, there is nothing here!'
#   if tasks:
#     return render(request, 'task_detail.html', {
#       'tasks': tasks,
#     })
#   else:
#     return render(request, 'task_detail.html', {
#     'error': error
#     })

@login_required
def task_detail(request, task_id):
  if request.method == 'GET':
    try:
      task = get_object_or_404(Task, pk=task_id, user=request.user)
      form = Task_form(instance=task)
      return render(request, 'task_detail.html', {
        'task': task,
        'form': form
      })
    except:
      error = 'Ohh, there is nothing here!'
      return render(request, 'task_detail.html', {
        'error': error,
      })
  else:
    try:
      task = get_object_or_404(Task, pk=task_id, user=request.user)
      form = Task_form(request.POST, instance=task)
      form.save()
      if task.datecompleted == None:
        return redirect('tasks')
      else:
        return redirect('tasks_completed')
    except ValueError:
      return render(request, 'task_detail.html', {
        'task': task,
        'form': form,
        'error': 'Error updating task'
      })

@login_required
def complete_task(request, task_id):
  if request.method == 'POST':
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.datecompleted = timezone.now()
    task.save()
    return redirect('tasks')

@login_required
def delete_task(request, task_id):
  if request.method == 'POST':
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('tasks')

@login_required
def create_task(request):
  if request.method == 'GET':
    return render(request, 'create_task.html', {
      'form': Task_form
    })
  else:
    try:
      form = Task_form(request.POST)
      new_task = form.save(commit=False)
      new_task.user = request.user
      new_task.save()
      print(request.POST)
      return redirect('tasks')
    except ValueError:
      return render(request, 'create_task.html', {
      'form': Task_form,
      'error': 'Please provide valid data'
    })

@login_required
def sighout(request):
  logout(request)
  return redirect('home')

def signin(request):
  if request.method == 'GET':
    return render(request, 'signin.html', {
      'form': AuthenticationForm
    })
  else:
    user = authenticate(
      request,
      username=request.POST['username'],
      password=request.POST['password']
    )
    if user is None:
      return render(request, 'signin.html', {
        'form': AuthenticationForm,
        'error': 'Username or password is incorrect'
      })
    else:
      login(request, user)
      return redirect('tasks')