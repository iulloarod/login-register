from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.http import request
from .models import User
from datetime import datetime, date
import bcrypt


def index(request):
    return render(request, 'index.html')


def registration(request):
    if request.method == 'POST':
        #creating session to mantain input info if an error occurs
        request.session['reg_fname'] = request.POST['first_name']
        request.session['reg_lname'] = request.POST['last_name']
        request.session['reg_email'] = request.POST['email']
        #error for validation
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        # email duplicate finder
        new_email_check = request.POST['email']
        print(new_email_check) 
        registered_mail = User.objects.filter(email=new_email_check)
        if registered_mail :
            messages.error(request,"ERROR: This email already exists.")
            return redirect('/')
        # droping session info (where do I put it)
        request.session['reg_fname'] = ""
        request.session['reg_lname'] = ""
        request.session['reg_email'] = ""
        #  hashing the password
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print (pw_hash)
        # having checked for erorrs, checked if the email already existed and hashed the password, we now create the new user:
        new_user = User.objects.create(
                                        first_name = request.POST['first_name'],
                                        last_name=request.POST['last_name'],
                                        email=request.POST['email'],
                                        password=pw_hash
                                        )
        # creating session.user to use later
        request.session['user'] = {
                "id" : new_user.id,
                "name": f"{new_user.first_name} {new_user.last_name}",
                "email": new_user.email
            }
        messages.success(request, "Welcome User!")
        return redirect("/imin")


def login(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                user_logged = {
                    "id" : log_user.id,
                    "name": f"{log_user.first_name} {log_user.last_name}",
                    "email": log_user.email
                }
                request.session['user'] = user_logged
                messages.success(request, "Loged.")
                return redirect("/imin")
            else:
                messages.error(request, "Email or Password incorrect.")
        else:
            messages.error(request, "Email or Password incorrect.")
    return redirect("/")


def imin(request):
    #stopper for session if user is not logged in
    if 'user' not in request.session:
        messages.error(request,'FORBIDDEN ACCESS: User must be reggistered to enter.')
        return redirect("/")
    return render(request, 'imin.html')


def logout(request):
    request.session.flush()
    print(list(request.session.keys()))
    messages.success(request,'User logged out')
    return redirect("/")

