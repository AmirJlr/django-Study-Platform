from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from account.models import User

from base.models import Topic
from .forms import UserForm,MyUserCreationForm

# Create your views here.

@login_required
def userProfile(request, pk):
    user = User.objects.get(id= pk)

    # ..._set is for ForeignKey when we go through the key to all
    msgs = user.message_set.all()
    rooms = user.room_set.all()

    topics = Topic.objects.all()

    context ={
        'user':user,
        'msgs':msgs,
        'rooms':rooms,
        'topics':topics,
    }
    return render(request, 'account/profile.html', context)



@login_required
def editProfile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        # 1 Way:
        # username = request.POST.get('username')
        # email = request.POST.get('email')

        # user.username = username
        # user.email = email 
        # user.save()
        # return redirect('account:profile', user.id)

        #2 Way:
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:profile', user.id)


    context ={
        'form':form,
    }
    return render(request, 'account/edit-profile.html',context)
    

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('room:home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exists :/')

        user = authenticate(request, email=email, password= password)
        if user is not None:
            login(request, user)
            return redirect("room:home")
        else:
            messages.error(request, 'Username and Password does not match :/')

       
    context = {
        'page':page,
    }
    return render(request, 'account/login_register.html', context)



def logoutPage(request):
    logout(request)
    return redirect("room:home")



def registerPage(request):
    page = 'register'

    form = MyUserCreationForm()

    if request.user.is_authenticated:
        return redirect('room:home')

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            login(request, user)
            return redirect('room:home')
        else:
             messages.error(request, 'an error occurred during registration :/')


    context = {
        'page':page,
        'form':form,
    }
    return render(request, 'account/login_register.html', context)

    