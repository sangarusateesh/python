from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.db import connection
from . forms import RegistrationForm
from . models import users as UserProfile
from django.core.mail import send_mail
from datetime import datetime
import random
import string

def check_mysql_connection(request):
    try:
        with connection.cursor() as cursor:
            # Execute a simple SQL query to test the connection
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

        message = "MySQL database connection is successful! Result: {}".format(result)
    except Exception as e:
        message = "MySQL database connection failed. Error: {}".format(str(e))

    return render(request, 'check_mysql_connection.html', {'message': message})

def say_hello(request):
    return render(request, 'hello.html', {'name':'Local E-Commerce'})
    # return HttpResponse('Hello World!.')
    # Create your views here.

def login(request):
    return render(request, 'login.html', {'name':'Local E-Commerce | Login'})

def loginUser(request):
    username = request.POST.get('username')
    return render(request, 'profile.html',{'name':'Local E-Commerce | Login ','msg':'This User Name {username} not Registered with us.'.format(username=username),'statusCode':'Error'})

# @csrf_protect
def sign_up(request):
    
    # userName = request.POST.get('email')
    # userPass = request.POST.get('userPass')
    # if not userName:
    #     return render(request, 'login.html', {'name':'Local E-Commerce | Login'})
    # elif not userPass:
    #     return render(request, 'login.html', {'name':'Local E-Commerce | Login'})
    return render(request, 'profile.html',{'name':'Local E-Commerce | Profile'})

def OrderDetails(request):
    # OrderId = request.POST.get('orderId')
    # if not OrderId:
    #     return render()
    return render(request,'OrderDetails.html',{'name':'Local E-Commerce | Order Details','Link':''})

def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def login_user(request):
    return JsonResponse({'status':'OK','msg':'Your\'e Successfully Registered with us., Please Check Your Email!.'},safe=False)
    
def register_user(request):
    if request.method == 'POST':
        form = json.load(request) #Get data from POST request
        # form = json.loads(form)
        # return JsonResponse({'status':'NOT OK','data':type(form)},safe=False)
        
        # if form.is_valid():
        email = form['email']
        phone = form['phone']
        user_name = form['user_name']
        password = generate_password()
        current_datetime = datetime.now()
        user_id = f"LUSR_.{current_datetime.strftime('%Y%M%d.%H%M%S')}"

        # Check if the email is already registered
        if UserProfile.objects.filter(user_email=email).exists():
            return JsonResponse({'status':'NOT OK','error':'This Email Already Registered with us!.'},safe=False)
        
        if UserProfile.objects.filter(userPhone=phone).exists():
            response_data = {
                'status': 'NOT OK',
                'msg': 'This Phone Number Already Registered with us.!'
            }
            return JsonResponse({'status':'NOT OK','error':'This Phone Number Already Registered with us.!'},safe=False)
            
        new_Record = UserProfile(
            user_id     = user_id,
            user_name   = user_name,
            user_email  = email,
            userPhone   = phone,
            passCode    = password,
        )
        new_Record.save()
        sendEmail(email,password)
        return JsonResponse({'status':'OK','msg':'Your\'e Successfully Registered with us., Please Check Your Email!.'},safe=False)
    else:
        return JsonResponse({'status':'OK','error':'Something Went to Wrong Please try again!.'},safe=False)
            

def sendEmail(email,password):
    # Your email settings
    subject = 'Welcome to L-Commerce'
    message = 'Your\'e Registered Successfully with us.<br>Login Credentials<br>User Name: {email}<br>Password: {password}'.format(email=email,password=password)
    sender_email = 'your_email@gmail.com'  # Your Gmail email address
    recipient_email = email  # Recipient's email address
    # Optionally, you can catch any exceptions that may occur during sending
    try:
        send_mail(
            subject,
            message,
            sender_email,
            [recipient_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        return False
