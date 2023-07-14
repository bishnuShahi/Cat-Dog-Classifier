from django.conf import settings
import tensorflow as tf
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from PIL import Image
import numpy as np
from .forms import MyForm


model = tf.keras.models.load_model("model.h5")


def index(request):
    return render(request, 'Authenticator/index.html')


def main(request):
    
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            image = Image.open(instance.image)
            image = image.resize((256, 256))
            image = np.array(image)
            image = image.reshape((1, 256, 256, 3))
            pred = model.predict(image)
            # pred = pred.flatten()

            return render(request, 'Authenticator/main.html', {'pred' : pred})
         
    return render(request, 'Authenticator/main.html')
    

def signup(request):

    if request.method == 'POST':
        uname = request.POST.get('uname')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        confirmPass = request.POST.get('confirmPass')

        user = User.objects.create_user(uname, email, password)
        user.first_name = name

        #Saving the user
        user.save() 

        messages.success(request, 'Your account has been successfully created! ')

        return redirect('signin')

    return render(request, 'Authenticator/signup.html')

def signin(request):

    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('pass')

        user = authenticate(request, username=uname, password=password)

        if user != None:
            login(request, user)
            name = {'name' : user.first_name}
            messages.success(request, 'You have succesfully Logged in!')
            return render(request, "Authenticator/index.html", name)

        else:
            messages.error(request, "Incorrect username or password!")
            return redirect('signin')

    return render(request, 'Authenticator/signin.html')


def signout(request):
    logout(request)
    messages.success(request, 'You have logged out successfully!')
    return redirect('index')
