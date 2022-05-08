from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForms
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1']) # either of the passwords key can be used
                user.save()
                login(request, user)
                return redirect(currenttodos)

            except IntegrityError:
                return render(request, 'todo/signupuser.html',
                              {'form': UserCreationForm(), 'error': 'username has already been taken, please enter a unique username'})

        else:
            # passwords didn't match
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords entered did not match'})
            # error dictionary i have created could be anything not just error


@login_required
def currenttodos(request):
    todos_initialize = Todo.objects.filter(user=request.user, date_completed__isnull=True) # initialize only user wise not all hence filter does that for us
    return render(request, 'todo/currenttodos.html', {'todos': todos_initialize})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect(home)


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None: # this means if the above user fails to authenticate username and password
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'user name and password did not match'})
        else:
            login(request, user)
            return redirect(currenttodos)


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/create.html', {'form': TodoForms}) # form is the context here we need to create our own form/context
    # what do we need to be saved from the user on the website
    else:
            form = TodoForms(request.POST) # if the user saves or posts the page
            save_without_user = form.save(commit=False) # we dont want to save before linking it to the user
            save_without_user.user = request.user
            save_without_user.save() # now we commit the save and render the user to the current page
            return redirect(currenttodos)
            # todo raise ValueError


@login_required
def viewtodo(request, todo_pk):
    todo_edit = get_object_or_404(Todo, pk=todo_pk, user=request.user) # we want to make sure users can only access their todos
    # we want to display the filled out form from the database hence we cant make use of form.py here instead
    # we could make an instance of todo_edit as that is initialized to class Todo and has all the information
    if request.method == 'GET':
        form = TodoForms(instance=todo_edit) # now our forms.py todoforms class will have filled out information from db
        return render(request, 'todo/viewtodo.html', {'todo_view': todo_edit, 'form': form})
    # first dict todo_view only prints the information but for us to edit something we need another
    # dict which is form
    else:
        form = TodoForms(request.POST, instance=todo_edit) # mapping our instance to the initialized class
        form.save()
        # todo raise ValueError with try and except
        return redirect('currenttodos')


@login_required
def completedtodo(request, todo_pk):
    todo_edit = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo_edit.date_completed = timezone.now()
        todo_edit.save()
        return redirect('currenttodos')


@login_required
def deletedtodo(request, todo_pk):
    todo_edit = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo_edit.delete()
        return redirect('currenttodos')


@login_required
def viewcompletedtodos(request):
    todos_initialize = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed') # date_completed false will only reflect completed todos
    return render(request, 'todo/completed.html', {'todos': todos_initialize})

