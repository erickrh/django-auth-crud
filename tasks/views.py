from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.http import HttpResponse
from .forms import Task_form
from .models import Task

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

def tasks(request):
  # tasks = Task.objects.all()
  tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
  return render(request, 'tasks.html', {
    'tasks': tasks
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

def task_detail(request, task_id):
  try:
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    return render(request, 'task_detail.html', {
      'task': task,
    })
  except:
    error = 'Ohh, there is nothing here!'
    return render(request, 'task_detail.html', {
      'error': error,
    })

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
      return render(request, signin.html, {
        'form': AuthenticationForm,
        'error': 'Username or password is incorrect'
      })
    else:
      login(request, user)
      return redirect('tasks')