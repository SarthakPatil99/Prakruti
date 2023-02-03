from django.shortcuts import render, redirect, HttpResponse
from .models import Users, Appointments, M_remedy, H_remedy, Blogs, Orders, Med_per_ord,Cart
from django.contrib.auth.models import User, auth
# from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.utils.datastructures import MultiValueDictKeyError
from sqlalchemy import null
import random
from datetime import date

jinja = {}

# -----------------------------Getters and setters---------------------------


def getPrakruti(val):
    if val == '1':
        return ("Vata", "Kapha")
    elif val == '2':
        return ("Vata", "Pitta")
    elif val == '3':
        return ("Kapha", "Vata")
    elif val == '4':
        return ("Kapha", "Pitta")
    elif val == '5':
        return ("Pitta", "Vata")
    else:
        return ("Pitta", "Kapha")


def getGender(gender):
    if (gender == "1"):
        return "male"
    elif (gender == "2"):
        return "female"
    elif (gender == "3"):
        return "other"


# -----------------------------Main functions---------------------------
def index(request):
    return render(request, 'index.html')


def signup(request):
    return render(request, 'signup.html')


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
        print(urname, fname, mname, lname, email,
              phone, pwd, cpwd, age, gender, picture)
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
            new_user = Users(UserName=urname, Middle_name=mname,
                             Phone_No=phone, Age=age, Gender=gender, Img=picture)
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
            User.objects.filter(email=chPassMail).update(password=conf_pass)
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
    if request.POST:
        print(request.POST)
        if request.POST['submit']:
            new_cart = Cart(Username= request.user.username,p_id=request.POST['submit'])
            new_cart.save()

    pds = M_remedy.objects.all()
    return render(request, 'user/Shopping.html',{'prods':pds})


def U_profile(request):
    return render(request, 'user/U_profile.html', {'admin': 0})


def profileU(request):
    return render(request, 'user/U_profile.html', {'admin': 1})


def cart(request):
    crt = []
    if request.POST:
        print(request.POST)
        if request.POST['remove']:
            Cart.objects.get(id=request.POST['remove']).delete()

    pds = Cart.objects.filter(Username = request.user.username )
    for pd in pds:
        temp = vars(M_remedy.objects.get(pk = pd.p_id))
        temp['cartid']= pd.pk
        crt.append(temp)
    print(crt)
    return render(request, 'user/Cart.html',{'Cart':crt})


def our_blogs(request):
    type = ["BLOG", "IMAGE", "VIDEO"]
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        try:
            title = request.POST['Title']
            Btype = type[int(request.POST['Btype'])-1]
            File = " "
            content = ' '
            print("------------------0")
            dt = date.today()
            print("------------------1")
            if Btype == 'BLOG':
                content = request.POST['content']
            else:
                try:
                    File = request.FILES['inFile']
                except:
                    File = request.POST['ImgURL']
                print("------------------2")
            print("------------------3")
            if request.POST['submit'] == 'Modify':
                # update blog code
                b_id = request.POST['bid']
                update_blog = Blogs.objects.get(id=b_id)
                update_blog.Title = title
                update_blog.Type = Btype
                update_blog.Content = content
                update_blog.Date = dt
                update_blog.file = File
                update_blog.save()
                pass
            if request.POST['submit'] == 'Create':
                # add blog code
                new_blog = Blogs(Title=title, Type=Btype, Content=content, Date=dt, file=File)
                new_blog.save()
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)
        # view
    Bls = Blogs.objects.all()
    return render(request, 'user/our_blogs.html', {'Bls': Bls})

# -----------------------------ADMIN SIDE---------------------------


def dashboard(request):
    Pts = Users.objects.all()
    MRs = M_remedy.objects.all()
    HRs = H_remedy.objects.all()
    Bls = Blogs.objects.all()

    Apts = Appointments.objects.all()
    CApts = Appointments.objects.filter(Status_A=True)
    Ords = Orders.objects.all()
    COrds = Orders.objects.filter(Status=True)

    all_data = {}
    all_data['pts_ct'] = len(Pts)
    all_data['mrs_ct'] = len(MRs)
    all_data['hrs_ct'] = len(HRs)
    all_data['bls_ct'] = len(Bls)
    try:
        all_data['apts_ct'] = (len(CApts) / len(Apts))*100
    except:
        all_data['apts_ct'] = 0
    try:
        all_data['ords_ct'] = (len(COrds) / len(Ords))*100
    except:
        all_data['ords_ct'] = 0

    print(all_data)
    return render(request, 'admin/Dashboard.html', {'data': all_data})


def patients(request):
    
    new_pts = []
    Pts = Users.objects.all()

    if request.method == 'POST':
        print(request.POST)
        try:
            if request.POST['search']:
                if request.POST['srch'] == '1':
                    Pts = Users.objects.all()
                    string =request.POST['search'].lower()
                    for Pt in Pts:
                        Pt_exts = User.objects.filter(username=Pt.UserName)
                        for Pt_ext in Pt_exts:
                            strs = (Pt_ext.first_name+" "+Pt.Middle_name+" " + Pt_ext.last_name)
                            strs = strs.lower()
                            print(string,strs)
                            if string in strs:
                                new_pt = vars(Pt)
                                new_pt.update(vars(Pt_ext))
                                new_pt.pop('_state')
                                new_pt.pop('password')
                                new_pt.pop('last_login')
                                new_pt.pop('is_superuser')
                                new_pt.pop('is_staff')
                                new_pt.pop('is_active')
                                new_pt.pop('date_joined')
                                new_pt.pop('UserName')
                                new_pts.append(new_pt)
                    return render(request, 'admin/patients.html', {'patients': new_pts})
                if request.POST['srch'] == '2':
                    try:
                        Pt = Users.objects.get(pk=request.POST['search'])
                        Pt_ext = User.objects.get(username=Pt.UserName)
                        new_pt = vars(Pt)
                        new_pt.update(vars(Pt_ext))
                        new_pt.pop('_state')
                        new_pt.pop('password')
                        new_pt.pop('last_login')
                        new_pt.pop('is_superuser')
                        new_pt.pop('is_staff')
                        new_pt.pop('is_active')
                        new_pt.pop('date_joined')
                        new_pt.pop('UserName')
                        new_pts.append(new_pt)
                        return render(request, 'admin/patients.html', {'patients': new_pts})
                    except:
                        return render(request, 'admin/patients.html', {'patients': new_pts})
                if request.POST['srch'] == '3':
                    Pts = User.objects.filter(email__contains=request.POST['search'])
                    for Pt in Pts:
                        Pt_ext = Users.objects.filter(UserName=Pt.username)
                        if Pt_ext:
                            new_pt = vars(Pt)
                            for vr in Pt_ext:
                                new_pt.update(vars(vr))
                            new_pt.pop('_state')
                            new_pt.pop('password')
                            new_pt.pop('last_login')
                            new_pt.pop('is_superuser')
                            new_pt.pop('is_staff')
                            new_pt.pop('is_active')
                            new_pt.pop('date_joined')
                            new_pt.pop('UserName')
                            new_pts.append(new_pt)
                    return render(request, 'admin/patients.html', {'patients': new_pts})
                if request.POST['srch'] == '4':
                    Pts = Users.objects.filter(Phone_No__contains=request.POST['search'])
                    for Pt in Pts:
                        Pt_ext = User.objects.filter(username=Pt.UserName)
                        if Pt_ext:
                            new_pt = vars(Pt)
                            for vr in Pt_ext:
                                new_pt.update(vars(vr))
                            new_pt.pop('_state')
                            new_pt.pop('password')
                            new_pt.pop('last_login')
                            new_pt.pop('is_superuser')
                            new_pt.pop('is_staff')
                            new_pt.pop('is_active')
                            new_pt.pop('date_joined')
                            new_pt.pop('UserName')
                            new_pts.append(new_pt)
                    return render(request, 'admin/patients.html', {'patients': new_pts})
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)
            
        try:
            if request.POST['submit']:
                # add patient code
                fname = request.POST['fname']
                mname = request.POST['mname']
                lname = request.POST['lname']
                email = request.POST['email']
                phone = request.POST['phone']
                age = request.POST['age']
                gender = getGender(request.POST['gender'])
                P_prakruti, S_prakruti = getPrakruti(request.POST['prakruti'])

                # Generate Username
                urname = fname+str(random.randint(00, 99))
                while User.objects.filter(username=urname):
                    urname = fname+str(random.randint(00, 99))

                # Generate Passward
                splChar = ['^', '%', '$', '#', '!', '@', '&']
                pwd = fname+random.choice(splChar)+str(random.randint(00, 99))

                # create User
                user = User.objects.create_user(
                    username=urname, password=pwd, email=email, first_name=fname, last_name=lname)
                user.save()
                new_user = Users(UserName=urname, Middle_name=mname,
                                Phone_No=phone, Age=age, Gender=gender, P_Prakruti=P_prakruti, S_Prakruti=S_prakruti)
                new_user.save()
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)

        try:
            if request.POST['remove']:
                # remove patient code
                Ur = Users.objects.get(UserName=request.POST['remove'])
                User.objects.get(username=request.POST['remove']).delete()
                Apts = Appointments.objects.filter(U_id=Ur.pk)
                for Apt in Apts:
                    Apt.delete()
                Ords = Orders.objects.filter(UserName=request.POST['remove'])
                for ord in Ords:
                    mds = Med_per_ord.objects.filter(o_id=ord.o_id)
                    for md in mds:
                        md.delete()
                    ord.delete()
                Ur.delete()
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)

    #     try:
    #         if request.POST['book']:
    #             # appintment booking code
    #             pass
    #     except MultiValueDictKeyError:
    #         print(MultiValueDictKeyError)

    # view
    
    for Pt in Pts:
        Pt_ext = User.objects.filter(username=Pt.UserName)
        if Pt_ext:
            new_pt = vars(Pt)
            for vr in Pt_ext:
                new_pt.update(vars(vr))
            new_pt.pop('_state')
            new_pt.pop('password')
            new_pt.pop('last_login')
            new_pt.pop('is_superuser')
            new_pt.pop('is_staff')
            new_pt.pop('is_active')
            new_pt.pop('date_joined')
            new_pt.pop('UserName')
            new_pts.append(new_pt)

    return render(request, 'admin/patients.html', {'patients': new_pts})


def appointments(request):
    new_apts = []
    if request.method == 'POST':
        print(request.POST)
        try:
            if request.POST['search']:
                if request.POST['srch'] == '1':
                    Apts = Appointments.objects.all()
                    for Apt in Apts:
                        string =request.POST['search'].lower()
                        Pt = Users.objects.get(id=Apt.U_id)
                        Pt_exts = User.objects.filter(username=Pt.UserName)
                        for Pt_ext in Pt_exts:
                            strs = (Pt_ext.first_name+" "+Pt.Middle_name+" " + Pt_ext.last_name)
                            strs = strs.lower()
                            print(string,strs)
                            if string in strs:
                                new_apt = vars(Apt)
                                new_apt['full_name'] = Pt.first_name+' ' + \
                                    Pt_ext.Middle_name+' '+Pt.last_name
                                new_apt['email'] = Pt.email
                                new_apt['phno'] = Pt_ext.Phone_No
                                new_apt['age'] = Pt_ext.Age
                                new_apt['gender'] = Pt_ext.Gender
                                new_apt.pop('_state')
                                new_apts.append(new_apt)
                    return render(request, 'admin/appointments.html', {'Apts': new_apts})
                if request.POST['srch'] == '2':
                    try:
                        Apts = Appointments.objects.all()
                        for Apt in Apts:
                            Pts = Users.objects.get(pk = request.POST['search']).get(id=Apt.U_id)
                            for Pt in Pts:
                                Pt_ext = User.objects.get(username=Pt.UserName)
                                new_apt = vars(Apt)
                                new_apt['full_name'] = Pt.first_name+' ' + \
                                    Pt_ext.Middle_name+' '+Pt.last_name
                                new_apt['email'] = Pt.email
                                new_apt['phno'] = Pt_ext.Phone_No
                                new_apt['age'] = Pt_ext.Age
                                new_apt['gender'] = Pt_ext.Gender
                                new_apt.pop('_state')
                                new_apts.append(new_apt)
                        return render(request, 'admin/appointments.html', {'Apts': new_apts})
                    except:
                        return render(request, 'admin/appointments.html', {'Apts': new_apts})
                if request.POST['srch'] == '3':
                    Apts = Appointments.objects.all()
                    for Apt in Apts:
                        Pts = Users.objects.filter(email__contains = request.POST['search']).get(id=Apt.U_id)
                        for Pt in Pts:
                            Pt_ext = User.objects.get(username=Pt.UserName)
                            new_apt = vars(Apt)
                            new_apt['full_name'] = Pt.first_name+' ' + \
                                Pt_ext.Middle_name+' '+Pt.last_name
                            new_apt['email'] = Pt.email
                            new_apt['phno'] = Pt_ext.Phone_No
                            new_apt['age'] = Pt_ext.Age
                            new_apt['gender'] = Pt_ext.Gender
                            new_apt.pop('_state')
                            new_apts.append(new_apt)
                    return render(request, 'admin/appointments.html', {'Apts': new_apts})
                if request.POST['srch'] == '4':
                    Apts = Appointments.objects.all()
                    for Apt in Apts:
                        Pts = Users.objects.filter(Phone_No__contains = request.POST['search']).get(id=Apt.U_id)
                        for Pt in Pts:
                            Pt_ext = User.objects.get(username=Pt.UserName)
                            new_apt = vars(Apt)
                            new_apt['full_name'] = Pt.first_name+' ' + \
                                Pt_ext.Middle_name+' '+Pt.last_name
                            new_apt['email'] = Pt.email
                            new_apt['phno'] = Pt_ext.Phone_No
                            new_apt['age'] = Pt_ext.Age
                            new_apt['gender'] = Pt_ext.Gender
                            new_apt.pop('_state')
                            new_apts.append(new_apt)
                    return render(request, 'admin/appointments.html', {'Apts': new_apts})
                if request.POST['srch'] == '5':
                    Apts = Appointments.objects.all()
                    for Apt in Apts:
                        Pts = Users.objects.filter(Age__gte = request.POST['search']).get(id=Apt.U_id)
                        for Pt in Pts:
                            Pt_ext = User.objects.get(username=Pt.UserName)
                            new_apt = vars(Apt)
                            new_apt['full_name'] = Pt.first_name+' ' + \
                                Pt_ext.Middle_name+' '+Pt.last_name
                            new_apt['email'] = Pt.email
                            new_apt['phno'] = Pt_ext.Phone_No
                            new_apt['age'] = Pt_ext.Age
                            new_apt['gender'] = Pt_ext.Gender
                            new_apt.pop('_state')
                            new_apts.append(new_apt)
                    return render(request, 'admin/appointments.html', {'Apts': new_apts})
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)
    #     try:
    #         if request.POST['submit'] == 'Schedule':
    #             Aid = request.POST['apptID']
    #             Appnt = request.POST['appnt']
    #             Date = request.POST['date']

    #             # appintment reschedule code
    #             # new_apt = Appointments.objects.filter(id=Pid).update(Date=Date, TimeSlot=Appnt)
    #             # new_apt.save()
    #             pass
    #         else:
    #             Pid = request.POST['apptID']
    #             Presc = request.POST['Description']

    #             # add prescription code
    #             # new_apt = Appointments.objects.filter(id=Pid).update(P_med=Presc)
    #             # new_apt.save()
    #             pass
    #     except MultiValueDictKeyError:
    #         print(MultiValueDictKeyError)

        try:
            if request.POST['remove']:
                # remove appintment code
                Appointments.objects.get(id=request.POST['remove']).delete()
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)

    # view
    Apts = Appointments.objects.all()
    for Apt in Apts:
        patient_ext = Users.objects.get(id=Apt.U_id)
        patient = User.objects.get(username=patient_ext.UserName)
        new_apt = vars(Apt)
        new_apt['full_name'] = patient.first_name+' ' + \
            patient_ext.Middle_name+' '+patient.last_name
        new_apt['email'] = patient.email
        new_apt['phno'] = patient_ext.Phone_No
        new_apt['age'] = patient_ext.Age
        new_apt['gender'] = patient_ext.Gender
        new_apt.pop('_state')
        new_apts.append(new_apt)
    print(new_apts)
    # print(Apts)
    return render(request, 'admin/appointments.html', {'Apts': new_apts})


def M_remedies(request):
    
    if request.method == 'POST':
        print(request.POST)
        try:
            if request.POST['search']:
                if request.POST['srch'] == '1':
                    MRs = M_remedy.objects.filter(Name__contains = request.POST['search'] )
                    return render(request, 'admin/M_remedies.html', {'MRs': MRs})
                if request.POST['srch'] == '2':
                    try:
                        MRs = M_remedy.objects.filter(id = request.POST['search'])
                        return render(request, 'admin/M_remedies.html', {'MRs': MRs})
                    except:
                        MRs = []
                        return render(request, 'admin/M_remedies.html', {'MRs': MRs})
                if request.POST['srch'] == '3':
                    MRs = M_remedy.objects.filter(Price__gte = int(request.POST['search']))
                    return render(request, 'admin/M_remedies.html', {'MRs': MRs})
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)
        try:
            name = request.POST['name']
            description = request.POST['description']
            contents = request.POST['contents']
            quantity = request.POST['quantity']
            price = request.POST['price']
            try:
                picture = request.FILES['inFile']
            except:
                picture = request.POST['ImgURL']
            if request.POST['submit'] == 'Modify':
                # update medicine code
                m_id = request.POST['mid']
                update_med = M_remedy.objects.get(id=m_id)
                update_med.Name = name
                update_med.Desc = description
                update_med.Content = contents
                update_med.Quantity = quantity
                update_med.Price = price
                update_med.Img = picture
                update_med.save()
                pass
            if request.POST['submit'] == 'Create':
                # add medicine code
                new_med = M_remedy(Name=name, Desc=description, Content=contents,
                                    Quantity=quantity, Price=price, Img=picture)
                new_med.save()
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)

        try:
            if request.POST['remove']:
                # remove medicine code
                mr = M_remedy.objects.get(id=request.POST['remove'])
                mds = Med_per_ord.objects.filter(m_id = mr.pk)
                for md in mds:
                    md.m_id = -1
                    md.save()
                mr.delete()
                pass
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)

    # view
    MRs = M_remedy.objects.all()
    # print(MRs)
    return render(request, 'admin/M_remedies.html', {'MRs': MRs})


def H_remedies(request):
    # view
    HRs = H_remedy.objects.all()
    # print(HRs)

    if request.method == 'POST':
        print(request.POST)
        try:
            if request.POST['search']:
                if request.POST['srch'] == '1':
                    HRs = H_remedy.objects.filter(Name__contains = request.POST['search'] )
                    return render(request, 'admin/H_remedies.html', {'HRs': HRs})
                if request.POST['srch'] == '2':
                    try:
                        HRs = H_remedy.objects.filter(id = request.POST['search'])
                        return render(request, 'admin/H_remedies.html', {'HRs': HRs})
                    except:
                        HRs = []
                        return render(request, 'admin/H_remedies.html', {'HRs': HRs})
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)
        try:
            title = request.POST['title']
            desc = request.POST['description']
            acce = request.POST['accessaries']
            try:
                picture = request.FILES['inFile']
            except:
                picture = request.POST['ImgURL']
            if request.POST['submit'] == 'Modify':
                # update remedy code
                h_id = request.POST['hid']
                update_hmed = H_remedy.objects.get(id=h_id)
                update_hmed.Name = title
                update_hmed.Desc = desc
                update_hmed.Accessories = acce
                update_hmed.Img = picture
                update_hmed.save()
                pass
            if request.POST['submit'] == 'Create':
                # add remedy code
                new_hmed = H_remedy(Name=title, Desc=desc, Accessories=acce, Img=picture)
                new_hmed.save()
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)

        try:
            if request.POST['remove']:
                # remove remedy code
                H_remedy.objects.filter(id=request.POST['remove']).delete()
                pass
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)

    return render(request, 'admin/H_remedies.html', {'HRs': HRs})


def blogs(request):
    type = ["BLOG", "IMAGE", "VIDEO"]
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        try:
            if request.POST['search']:
                # if request.POST['srch'] == '1':
                Bls = Blogs.objects.filter(Title__contains = request.POST['search'] )
                return render(request, 'admin/blogs.html', {'Bls': Bls})
                # if request.POST['srch'] == '2':
                #     try:
                #         Bls = Blogs.objects.filter(id = request.POST['search'])
                #         return render(request, 'admin/blogs.html', {'Bls': Bls})
                #     except:
                #         Bls = []
                #         return render(request, 'admin/blogs.html', {'Bls': Bls})
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)
        try:
            title = request.POST['Title']
            Btype = type[int(request.POST['Btype'])-1]
            File = " "
            content = ' '
            print("------------------0")
            dt = date.today()
            print("------------------1")
            if Btype == 'BLOG':
                content = request.POST['content']
            else:
                try:
                    File = request.FILES['inFile']
                except:
                    File = request.POST['ImgURL']
                print("------------------2")
            print("------------------3")
            if request.POST['submit'] == 'Modify':
                # update blog code
                b_id = request.POST['bid']
                update_blog = Blogs.objects.get(id=b_id)
                update_blog.Title = title
                update_blog.Type = Btype
                update_blog.Content = content
                update_blog.Date = dt
                update_blog.file = File
                update_blog.save()
                pass
            if request.POST['submit'] == 'Create':
                # add blog code
                new_blog = Blogs(Title=title, Type=Btype, Content=content, Date=dt, file=File)
                new_blog.save()
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)

        try:
            if request.POST['remove']:
                # remove blog code
                Blogs.objects.get(id=request.POST['remove']).delete()
                pass
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)

    # view
    Bls = Blogs.objects.all()
    return render(request, 'admin/blogs.html', {'Bls': Bls})


def orders(request):
    # view
    new_ords = []
    Ords = Orders.objects.all()
    for Ord in Ords:
        new_ord=vars(Ord)
        new_ord.pop('_state')
        patient = User.objects.get(username=Ord.UserName)
        patient_ext = Users.objects.get(UserName=patient.username)
        new_ord['full_name'] = patient.first_name+' ' + \
            patient_ext.Middle_name+' '+patient.last_name
        new_ord['email'] = patient.email
        new_ord['phno'] = patient_ext.Phone_No
        Pids = Med_per_ord.objects.filter(o_id=Ord.o_id)
        Prds = []
        for Pid in Pids:
            temp = {}
            Prd = M_remedy.objects.get(id=Pid.m_id)
            temp['name']=Prd.Name
            temp['price']=Prd.Price
            temp['quantity']= 0
            temp['m_id']=Pid.m_id
            temp['m_name']=Pid.m_name
            Prds.append(temp)
        new_ord['products']=Prds
        new_ords.append(new_ord)
    if request.POST:
        try:
            if request.POST['remove']:
                # remove order code
                ord =Orders.objects.get(id=request.POST['remove'])
                mds = Med_per_ord.objects.filter(o_id = ord.o_id )
                for md in mds:
                    md.delete()
                ord.delete()
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)

    print(new_ords)
    return render(request, 'admin/Orders.html',{'orders':new_ords})


def A_profile(request):
    return render(request, 'admin/A_profile.html', {'admin': 0})


def profileA(request):
    return render(request, 'admin/A_profile.html', {'admin': 1})
