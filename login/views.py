from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

from django.views.generic import ListView, CreateView # new
from django.urls import reverse_lazy # new

from .forms import ImageForm, UpdateImageForm # new
from .models import User


# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        return redirect('/home')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/home')

def logout(request):
    request.session.clear()
    return redirect('/')

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'all_users': User.objects.all()
    }
    return render(request, 'home.html', context)

def profile(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'profile.html' , context)

def update(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        user_to_update                   = User.objects.get(id=user_id)
        user_to_update.first_name        = request.POST['first_name']
        user_to_update.last_name         = request.POST['last_name']
        user_to_update.email             = request.POST['email']
        #user_to_update.profile_pic       = request.POST['profile_pic']
        user_to_update.save()

    return redirect('/profile/' + str(user_id))

def update_photo(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        #pic_to_update = User.objects.get(id=user_id)
        #pic_to_update.profile_pic = request.POST['profile_pic']
        #pic_to_update.save()


        form = UpdateImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'post.html', {'form': form, 'img_obj': img_obj})
    else:
        form = UpdateImageForm()
    return render(request, 'post.html', {'form': form})