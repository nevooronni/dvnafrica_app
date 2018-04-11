from django.contrib.auth import authenticate, login #Django's inbuilt authentication models
from django.contrib.auth.models import User  # Django Build in User Model
from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message # Our Message model
from chat.serializers import MessageSerializer, UserSerializer # Our Serializer Classes

# Create your views here.
#Users View
@csrf_exempt  # Decorator to make the view csrf exempt.
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:  # If PrimaryKey (id) of the user is specified in the url
            users = User.objects.filter(id=pk) # Select only that particular user
        else:
            users = User.objects.all() # Else get all user list
        serializer = UserSerializer(users, many=True, context={'request': request}) 
        return JsonResponse(serializer.data, safe=False)  # Return serialized data
    elif request.method == 'POST':
        data = JSONParser().parse(request)   # On POST, parse the request object to obtain the data in json
        serializer = UserSerializer(data=data) # Seraialize the data
        if serializer.is_valid():
            serializer.save() # Save it if valid
            return JsonResponse(serializer.data, status=201) # Return back the data on success
        return JsonResponse(serializer.errors, status=400)  # Return back the errors  if not valid

@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def index(request):
    if request.user.is_authenticated: #redirect user to chat console 
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == 'POST': #Authentication of user
        username, passoword = request.POST['username'], request.POST['password']#retrieving username and password from  the POST data
        user = authenticate(username=username, passoword=passoword)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('chats')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'chat/register.html', {})

def chats(request):
    pass

