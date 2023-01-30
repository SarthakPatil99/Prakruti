from django.shortcuts import render, redirect, HttpResponse
from .models import Users, Appointments ,M_remedy, H_remedy, Blogs
from django.contrib.auth.models import User, auth
# from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.utils.datastructures import MultiValueDictKeyError
from sqlalchemy import null
import random

jinja = {}


def index(request):
    return render(request, 'index.html')


def signup(request):
    return render(request, 'signup.html')

# Login Logout Signup Password Handling

def getGender(gender):
    if (gender == "1"): 
        return "male"
    elif (gender == "2"): 
        return "female"
    elif (gender == "3"): 
        return "other"

def handleSignUp(request):
    print('----------------------1')
    if request.method == 'POST':
        urname = request.POST['urname']
        fname = request.POST['fname']
        mname = request.POST['mname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        pwd = request.POST['pwd']
        cpwd = request.POST['confirm_pwd']
        age = request.POST['age']
        gender = getGender(request.POST['gender'])
        picture = request.FILES['inFile']
        print(urname,fname,mname,lname,email,phone,pwd,cpwd,age,gender,picture)
        print('-------------------------2')
        if User.objects.filter(username=urname):
            messages.error(
                request, "USERNAME ALREADY EXIST! PLEASE TRY SOME ANOTHER USERNAME")
            return redirect('/signup')

        if User.objects.filter(email=email):
            messages.error(
                request, "E-MAIL ALREADY EXIST! PLEASE TRY SOME ANOTHER E-MAIL")
            return redirect('/signup')

        user = User.objects.create_user(
            username=urname, password=pwd, email=email, first_name=fname, last_name=lname)
        user.save()
        
        try:
            new_user = Users(UserName = urname, Middle_name = mname, Phone_No=phone, Age=age, Gender=gender, Img=picture)
            new_user.save()
        except Exception:
            print(Exception)
        
        messages.success(
            request, "Your account has been successfully created.")
        return redirect('/')
    else:
        return render(request, 'signup.html')


def handleLogin(request):
    print("0")
    if request.method == 'POST':
        print(request.POST)
        print("0.1")
        log_usr = request.POST['log_username']
        log_pwd = request.POST['log_pwd']
        print("0.2", log_usr)
        user = auth.authenticate(username=log_usr, password=log_pwd)
        print("0.3", user)
        if user is not None:
            Whos = User.objects.filter(username__contains=user)
            auth.login(request, user)
            messages.success(request, 'Successfully Logged In.')
            print("1")
            for Who in Whos:
                print("hihihihih")
                print(Who.is_superuser)
                if Who.is_superuser:
                    # jinja["Who"] = Who.username
                    return render(request, 'admin/Dashboard.html', jinja)
                else:
                    jinja["Who"] = ""
                    return render(request, 'index.html', jinja)
        else:
            messages.error(request, 'Invalid Credentials, Please try again.')
            return redirect('/')
    return HttpResponse('404 - Not Found')


def handleLogout(request):
    jinja["Who"] = ""
    auth.logout(request)
    messages.success(request, 'Successfully Logged Out')
    return redirect('/')


def chPass(request):
    print("0")
    if request.method == 'POST':
        print(request.POST)
        chPassMail = request.POST['chPassMail']
        conf_pass = request.POST['confPass']

        try:
            print("in try")
            # User.objects.filter(email=chPassMail).update(password=conf_pass)
            return redirect('/')
        except Exception as e:
            print('somthing wrong', e)

    return redirect('/')

# -----------------------------USER SIDE---------------------------


def home(request):
    return HttpResponse('this is home')


def analyze(request):
    return render(request, 'user/Analyzer.html')


def recommend(request):
    return render(request, 'user/Reccomender.html')


def shopping(request):
    return render(request, 'user/Shopping.html')


def U_profile(request):
    return render(request, 'user/U_profile.html', {'admin': 0})


def profileU(request):
    return render(request, 'user/U_profile.html', {'admin': 1})


def cart(request):
    return render(request, 'user/Cart.html')


def our_blogs(request):
    return render(request, 'user/our_blogs.html')

# -----------------------------ADMIN SIDE---------------------------


def dashboard(request):
    return render(request, 'admin/Dashboard.html')


def patients(request):
    if request.method == 'POST':
        print(request.POST)
        # if request.POST['submit']:
        #     # add patient code
        #     fname = request.POST['fname']
        #     mname = request.POST['mname']
        #     lname = request.POST['lname']
        #     email = request.POST['email']
        #     phone = request.POST['phone']
        #     age = request.POST['age']
        #     gender = getGender(request.POST['gender'])
        #     P_prakruti, S_prakruti = getPrakruti(request.POST['prakruti'])

        #     pass
        # elif request.POST['remove']:
        #     #remove patient code
        #     pass
        # else:
        #     # appintment booking code
        #     pass
        render(request, 'admin/patients.html')
    return render(request, 'admin/patients.html')


def appointments(request):
    if request.method == 'POST':
        print(request.POST)
        # if request.POST['submit'] == 'Schedule':
        #     Pid = request.POST['apptID']
        #     Day = request.POST['day']
        #     Appnt = request.POST['appnt']
        #     Date = request.POST['date']
        #     # appintment booking code
        #     pass
        # elif request.POST['submit'] == 'addPresc':
        #     Pid = request.POST['apptID']
        #     Presc = request.POST['Description']
        #     # add prescription code
        #     pass
        # else:
        #     # remove appintment code
        #     pass

        render(request, 'admin/appointments.html')
    return render(request, 'admin/appointments.html')


def M_remedies(request):
    if request.method == 'POST':
        print(request.POST)
        
        if request.POST['submit'] == 'Modify':
            # update medicine code
            pass
        elif request.POST['submit'] == 'Create':
            # add medicine code
            pass
        else:
            # remove medicine code
            pass
        render(request, 'admin/M_remedies.html')
    return render(request, 'admin/M_remedies.html')


def H_remedies(request):
    if request.method == 'POST':
        print(request.POST)
        if request.POST['submit'] == 'Modify':
            # update remedy code
            pass
        elif request.POST['submit'] == 'Create':
            # add remedy code
            pass
        else:
            #remove remedy code
            pass
        render(request, 'admin/H_remedies.html')
    return render(request, 'admin/H_remedies.html')


def blogs(request):
    if request.method == 'POST':
        print(request.POST)
        if request.POST['submit'] == 'Modify':
            # update blog code
            pass
        elif request.POST['submit'] == 'Create':
            # add blog code
            pass
        else:
            #remove blog code
            pass
        render(request, 'admin/blogs.html')
    return render(request, 'admin/blogs.html')


def orders(request):
    if request.method == 'POST':
        # if request.POST['Remove']:
        #       remove order code
        pass
    render(request, 'admin/Orders.html')
    return render(request, 'admin/Orders.html')

def A_profile(request):
    # jinja["prof_who"] = request.user
    return render(request, 'admin/A_profile.html', {'admin': 0})

def profileA(request):
    return render(request, 'admin/A_profile.html', {'admin': 1})
