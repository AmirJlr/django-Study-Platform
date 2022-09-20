from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.utils.translation import activate

# Create your views here.

def change_lang(request):
    lang = request.GET.get('lang')
    next = request.GET.get('next')
    activate(lang)
    return redirect(next)

def home(request):
    # activate('fa')
    q = request.GET.get('q') or ''

    # search from side bar filter
    if q :
        rooms = Room.objects.filter(
            Q(topic__name__icontains = q) | Q(name__icontains=q) | Q(description__icontains=q)
        )
    else :
        rooms = Room.objects.all()
    ###

    room_count = rooms.count()
    msgs = Message.objects.filter(room__name__icontains = q)
    topics = Topic.objects.all()[:3]
    context = {
        'rooms':rooms,
        'room_count':room_count,
        'topics':topics,
        'msgs':msgs,
    }
    return render(request, 'base/home.html',context)

 

# in room detail
def room(request, pk):
    room = Room.objects.get(id = pk)

    # msgs = room.message_set.all()  from child to parent
    msgs = Message.objects.filter(room=room).order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        
        message = Message.objects.create(
            user = request.user,
            body = request.POST.get('body'),
            room=room,
        )
        room.participants.add(request.user)
        return redirect('room:room', pk = room.id)
        
    context = {
        'room':room,
        'msgs':msgs,
        'participants':participants,
        }
    
    return render(request, 'base/room.html', context)




@login_required
def createRoom(request):
    form = RoomForm()

    topics = Topic.objects.all()
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('room:home')

        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room=form.save(commit=False)
        #     room.host = request.user
        #     room.save()
            


    context ={
        'form':form,
        'topics':topics,
    } 
    return render(request, 'base/room_form.html', context)


@login_required
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host :
        return HttpResponse('You are not allowed !!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('room:home')

        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        #     return redirect('room:home')

    context = {
        'form':form,
        'topics':topics,
        'room':room,
    }
    return render(request, 'base/room_form.html', context)
    

@login_required
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host :
        return HttpResponse('You are not allowed !!')


    if request.method == 'POST':
        room.delete()
        return redirect('room:home')

    return render(request, 'base/delete.html', {'obj':room})  


@login_required
def deleteMsg(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user :
        return HttpResponse('You are not allowed !!')

    if request.method == 'POST':
        message.delete()
        return redirect('room:home')
    return render(request, 'base/delete.html', {'obj':message})



# for mobile responsive purpose

def topics(request):
    q = request.GET.get('q') or ''

    topics= Topic.objects.filter(name__icontains = q)

    context ={
        'topics':topics,
    }
    return render(request, 'base/topics.html', context)


def activity(request):
    msgs = Message.objects.all()
    context ={
        'msgs':msgs,
    }
    return render(request, 'base/activity.html', context)
