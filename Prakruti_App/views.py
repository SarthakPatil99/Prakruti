# from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse
from .models import Users, Appointments, M_remedy, H_remedy, Blogs, Orders, Prakruti_Quetions, Med_per_ord, Cart, Complaint_Quetions, Prakruti_Quetions_Ans
from django.contrib.auth.models import User, auth
from django.contrib import messages

from django.utils.datastructures import MultiValueDictKeyError
from sqlalchemy import null
import random
import calendar
from datetime import date, datetime, timedelta, time

jinja = {'pt_sort': 'id', 'bl_sort': 'id', 'apt_sort': 'id',
        'mr_sort': 'id', 'hr_sort': 'id', 'ord_sort': 'o_id'}

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


def getAvailableSlot(date, appointment):
    Apts = Appointments.objects.filter(Date=date, TimeSlot=appointment)
    if len(Apts) < 11:
        return 1
    else:
        return 0


def getNextAvailableSlot():
    i = 0
    while i < 5:
        dt = date.today() + timedelta(i)
        day = calendar.day_name[dt.weekday()]
        if day != "Sunday":
            slots = ["Morning", "Afternoon", "Evening"]
            if i == 0:
                currentTime = datetime.now()
                if currentTime.hour < 12:
                    j = 0
                elif 12 <= currentTime.hour < 18:
                    j = 1
                elif 18 <= currentTime.hour < 20:
                    j = 2
                else:
                    i += 1
                    continue
            else:
                j = 0
            while j < 3:
                Apts = Appointments.objects.filter(Date=dt, TimeSlot=slots[j])
                if len(Apts) < 10:
                    return dt, slots[j]
                j += 1
        i += 1
    return null, null

# -----------------------------Main functions---------------------------

def index(request):
    prds = M_remedy.objects.all().order_by('?')[:4]
    abc = ''
    try:
        abc = Users.objects.get(UserName = request.user)
    except:
        pass
    return render(request, 'index.html',{'prds':prds,'usr':abc})


def signup(request):
    return render(request, 'signup.html')


def mailVerify(request):
    print("in email", request.GET)
    if User.objects.filter(email=request.GET['email']):
        print('Email exists')
        return HttpResponse(True)
    else:
        print('Email does not exist')
        return HttpResponse(False)


def unameVerify(request):
    print("in uname", request.GET)
    if User.objects.filter(username=request.GET['uname']):
        print('username exists')
        return HttpResponse(True)
    else:
        print('username does not exist')
        return HttpResponse(False)


def handleSignUp(request):
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
    if request.method == 'POST':
        # print(request.POST)
        log_usr = request.POST['log_username']
        log_pwd = request.POST['log_pwd']
        print(request.POST)
        user = auth.authenticate(username=log_usr, password=log_pwd)
        if user is not None:
            Whos = User.objects.filter(username__contains=user)
            auth.login(request, user)
            messages.success(request, 'Successfully Logged In.')
            for Who in Whos:
                if Who.is_superuser:
                    # jinja["Who"] = Who.username
                    return redirect('/dashboard/')
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
    if request.POST:
        chPassMail = request.POST['chPassMail']
        conf_pass = request.POST['confPass']
        print(request.POST)

        try:
            user = User.objects.get(email=chPassMail)
            user.set_password(conf_pass)
            user.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('/')
        except Exception as e:
            messages.error(request, 'Invalid Credentials, Please try again.')
            print('somthing wrong', e)

    return redirect('/')

# -----------------------------USER SIDE---------------------------

def home(request):
    return HttpResponse('this is home')


def getKeys_dupVal(dictA):
    k_v_exchanged = {}

    for key, value in dictA.items():
        if value not in k_v_exchanged:
            k_v_exchanged[value] = [key]
        else:
            k_v_exchanged[value].append(key)

    return k_v_exchanged


def ageFilter(age, pks):
    if age > 0:
        prakruti = ""
        if age < 15:
            prakruti = "kapha"
        elif age < 46:
            prakruti = "pitta"
        else:
            prakruti = "vata"

        if prakruti in pks:
            return prakruti
        else:
            return 0
    return 0


def preferenceFilter(pks):
    prakruti = ['vata', 'pitta', 'kapha']
    newpks = []
    v1 = prakruti.index(pks[0])
    v2 = prakruti.index(pks[1])
    print(v1, v2)
    if v1 < v2:
        newpks.append(prakruti[v1])
        newpks.append(prakruti[v2])
    else:
        newpks.append(prakruti[v2])
        newpks.append(prakruti[v1])
    return newpks


def analyze(request):
    if request.POST:
        print(request.POST)
        age = Users.objects.get(UserName=request.user).Age
        pks = ['vata', 'pitta', 'kapha']
        prakruti = {}
        prakrutict = {
            'vata': 0,
            'pitta': 0,
            'kapha': 0
        }
        # print(request.POST)
        for i in range(1, 24):
            if request.POST[str(i)] == '1':
                prakrutict['vata'] += 1
            elif request.POST[str(i)] == '2':
                prakrutict['pitta'] += 1
            elif request.POST[str(i)] == '3':
                prakrutict['kapha'] += 1

        if prakrutict['vata'] == prakrutict['pitta'] == prakrutict['kapha']:
            prakruti['s'] = 4
        else:
            prakrutirpt = getKeys_dupVal(prakrutict)
            maxkey = max(prakrutirpt.keys())
            maxval = prakrutirpt[maxkey]

            # print(maxkey, type(maxkey), maxval, type(maxval))

            if len(maxval) > 1:
                prakruti['primary'] = ageFilter(age, maxval)
                # print(prakruti['primary'])
                if prakruti['primary']:
                    maxval.remove(prakruti['primary'])
                    prakruti['secondary'] = maxval[0]
                else:
                    newVals = preferenceFilter(maxval)
                    prakruti['primary'] = newVals[0]
                    prakruti['secondary'] = newVals[1]
            else:
                prakruti['primary'] = maxval[0]  # primary set

                minkey = min(prakrutirpt.keys())
                minval = prakrutirpt[minkey]
                # print(minkey, type(minkey), minval, type(minval))

                if len(minval) > 1:
                    prakruti['secondary'] = ageFilter(age, minval)
                    # print(prakruti['secondary'])
                    if not prakruti['secondary']:
                        newVals = preferenceFilter(minval)
                        prakruti['secondary'] = newVals[0]
                else:
                    prakruti['secondary'] = minval[0]
            user = Users.objects.get(UserName=request.user)
            user.P_Prakruti = prakruti['primary']
            user.S_Prakruti = prakruti['secondary']
            user.save()
            try:
                usr = Prakruti_Quetions_Ans.objects.get(u_id=request.user.id)
                usr.age=age
                usr.ans1=request.POST['1']
                usr.ans2=request.POST['2']
                usr.ans3=request.POST['3']
                usr.ans4=request.POST['4']
                usr.ans5=request.POST['5']
                usr.ans6=request.POST['6']
                usr.ans7=request.POST['7']
                usr.ans8=request.POST['8']
                usr.ans9=request.POST['9']
                usr.ans10=request.POST['10']
                usr.ans11=request.POST['11']
                usr.ans12=request.POST['12']
                usr.ans13=request.POST['13']
                usr.ans14=request.POST['14']
                usr.ans15=request.POST['15']
                usr.ans16=request.POST['16']
                usr.ans17=request.POST['17']
                usr.ans18=request.POST['18']
                usr.ans19=request.POST['19']
                usr.ans20=request.POST['20']
                usr.ans21=request.POST['21']
                usr.ans22=request.POST['22']
                usr.ans23=request.POST['23']
                usr.save()
            except:
                ans = Prakruti_Quetions_Ans(u_id=request.user.id, age=age, ans1=request.POST['1'], ans2=request.POST['2'],
                                            ans3=request.POST['3'], ans4=request.POST['4'], ans5=request.POST['5'], 
                                            ans6=request.POST['6'],ans7=request.POST['7'], ans8=request.POST['8'], 
                                            ans9=request.POST['9'], ans10=request.POST['10'],ans11=request.POST['11'], 
                                            ans12=request.POST['12'], ans13=request.POST['13'], ans14=request.POST['14'],
                                            ans15=request.POST['15'], ans16=request.POST['16'], ans17=request.POST['17'], 
                                            ans18=request.POST['18'], ans19=request.POST['19'], ans20=request.POST['20'], 
                                            ans21=request.POST['21'], ans22=request.POST['22'], ans23=request.POST['23'])
                ans.save()
        print(prakruti, prakrutict['vata'],prakrutict['pitta'], prakrutict['kapha'])
        return redirect('/recommend')
    Ques = Prakruti_Quetions.objects.all()
    return render(request, 'user/Analyzer.html', {'Quetions': Ques})


def recommend(request):
    prakruti = {}
    discription = {
        "PittaVata": "Pitta dosha includes processes responsible for metabolism, thermo-regulation, energy homeostasis, pigmentation, vision, and attentional processes and Vata dosha is the Ayurvedic mind-body element associated with air and space.",
        "PittaKapha": "Pitta dosha includes processes responsible for metabolism, thermo-regulation, energy homeostasis, pigmentation, vision, and attentional processes and Kapha dosha is the Ayurvedic mind-body element associated with earth and water.",
        "KaphaVata": "Kapha dosha is the Ayurvedic mind-body element associated with earth and water and Vata dosha is the Ayurvedic mind-body element associated with air and space.",
        "KaphaPitta": "Kapha dosha is the Ayurvedic mind-body element associated with earth and water and Pitta dosha includes processes responsible for metabolism, thermo-regulation, energy homeostasis, pigmentation, vision, and attentional processes.",
        "VataPitta": "Vata dosha is the Ayurvedic mind-body element associated with air and space and Pitta dosha includes processes responsible for metabolism, thermo-regulation, energy homeostasis, pigmentation, vision, and attentional processes.",
        "VataKapha": "Vata dosha is the Ayurvedic mind-body element associated with air and space and Kapha dosha is the Ayurvedic mind-body element associated with earth and water.",
        "Sama": "It is a combinetion of all prakruti Vata dosha is the Ayurvedic mind-body element associated with air and space, Pitta dosha includes processes responsible for metabolism, thermo-regulation, energy homeostasis, pigmentation, vision, and attentional processes and Kapha dosha is the Ayurvedic mind-body element associated with earth and water.",
    }
    # fetching prakruti of loggedin user
    user = Users.objects.get(UserName = request.user)
    prakruti['p'] = user.P_Prakruti.capitalize()
    prakruti['s'] = user.S_Prakruti.capitalize()
    prk = prakruti['p'] + prakruti['s']
    prakruti['d'] = discription[prk]
    print("prakruti:", prakruti)

    # fetching Questions
    Ques = Complaint_Quetions.objects.filter(prakruti = user.P_Prakruti)
    return render(request, 'user/Reccomender.html', {"prakruti": prakruti, 'Quetions': Ques})


def shopping(request):
    prakruti = {}
    try:
        # fetching prakruti of loggedin user
        user = Users.objects.get(UserName=request.user)
        prakruti['p'] = user.P_Prakruti
    except:
        pass
    print("prakruti:", prakruti)

    if request.POST:
        print(request.POST)
        try:
            if request.POST['recc']:
                print("recccccc")
                recc = int(request.POST['recc'])
                T=0
                for i in range(1,recc + 1):
                    if request.POST[str(i)]:
                        T += 1
                gen = Users.objects.get(UserName=request.user).Gender
                if gen == 'Male':
                    exc = M_remedy.objects.filter(Category = 'MEN\'S HEALTH')
                elif gen == 'Female':
                    exc = M_remedy.objects.filter(Category = 'WOMEN\'S HEALTH')
                else:
                    exc = M_remedy.objects.filter(Category = 'Skincare')
                # print(exc)
                recm = M_remedy.objects.all().order_by('?').difference(exc)
                if recc/2 >= T:
                    recm = recm[:T]
                else:
                    recm = recm[:recc-4]
                other = M_remedy.objects.all().difference(recm)
                # print(recm,"\n",other)
                print("out reccc")
                return render(request, 'user/Shopping.html', {'other': other,"recm":recm, "prakruti": prakruti})
        except MultiValueDictKeyError:
            print("Recommend: ", MultiValueDictKeyError)
        try:
            if request.POST['buy_now']:
                cts = Cart.objects.filter(Username=request.user).filter(
                    p_id=request.POST['buy_now'])
                for ct in cts:
                    print("olditem",ct, ct.quantity, ct.p_id)
                    ct.quantity = ct.quantity + 1
                    ct.save()
                    print("item added to cart of id", request.POST['buy_now'])
                    return redirect('/cart/')
                new_cart = Cart(Username=request.user,
                                p_id=request.POST['buy_now'], quantity=1)
                new_cart.save()
                print("new item added to cart of id", request.POST['buy_now'])
                return redirect('/cart/')
        except MultiValueDictKeyError:
            print("Buy now: ", MultiValueDictKeyError)

        try:
            if request.POST['cart']:
                cts = Cart.objects.filter(Username=request.user).filter(
                    p_id=int(request.POST['cart']))
                for ct in cts:
                    ct.quantity = ct.quantity + 1
                    print('olditem',ct,ct.quantity,ct.p_id)
                    ct.save()
                    print("item added to cart of id",request.POST['cart'])
                    messages.success(request, 'Item added to cart.')
                    pds = M_remedy.objects.all()
                    return render(request, 'user/Shopping.html', {'prods': pds})
                new_cart = Cart(Username=request.user,
                                p_id=request.POST['cart'],quantity=1)                
                new_cart.save()
                messages.success(request, 'Item added to cart.')
                print("new item added to cartid", request.POST['cart'])
        except MultiValueDictKeyError:
            print("Cart: ", MultiValueDictKeyError)

        try:
            if request.POST['category']:
                try:
                    category = request.POST.getlist('category')
                    pds = M_remedy.objects.filter(Category = "")
                    for cat in category:
                        pds = pds.union(M_remedy.objects.filter(Category=cat))
                    print(pds) 
                    return render(request, 'user/Shopping.html', {'other': pds, "prakruti": prakruti})
                except:
                    pass
        except:
            print("Categorize: ", MultiValueDictKeyError)

    pds = M_remedy.objects.all()
    return render(request, 'user/Shopping.html', {'other': pds, "prakruti": prakruti})


def U_profile(request):
    if request.POST:
        print(request.POST)
        print(request.FILES)
        try:
            if request.POST['submit']:
                usr = User.objects.get(username=request.user)
                usr_ext = Users.objects.get(UserName=usr.username)
                usr.first_name = request.POST['Fname']
                usr_ext.Middle_name = request.POST['Mname']
                usr.last_name = request.POST['Lname']
                usr.email = request.POST['Email']
                usr_ext.Phone_No = request.POST['Phone']
                usr_ext.Gender = getGender(request.POST['Gender'])
                usr_ext.Age = request.POST['Age']
                print('data accessed')
                try:
                    usr.P_Prakruti, usr.S_Prakruti = getPrakruti(request.POST['Prakruti'])
                except:
                    print('prakruti not found')
                try:
                    print('file', request.FILES['inFile'])
                    usr_ext.Img = request.FILES['inFile']
                except:
                    print('image not found')
                usr.save()
                usr_ext.save()
                print("____________________________________")
                print('user updated successfully')
                request.redirect('/U_profile')
        except Exception as e:
            print("Update: ", e.args)
    usr = User.objects.get(username=request.user.username)
    usr_ext = Users.objects.get(UserName=usr.username)
    Usrs = vars(usr)
    Usrs.update(vars(usr_ext))
    Usrs['appnts'] = Appointments.objects.filter(U_id=usr_ext.pk)
    if (request.user.is_superuser):
        Usrs['admin'] = 1
    else:
        Usrs['admin'] = 0
    return render(request, 'user/U_profile.html', {'users': Usrs})


def cart(request):
    crt = []
    if request.POST:
        print(request.POST)
        try:
            if request.POST['remove']:
                Cart.objects.get(id=request.POST['remove']).delete()
                messages.error(request, 'Item deleted from cart.')
        except MultiValueDictKeyError:
            print("Remove: ", MultiValueDictKeyError)
        
        try:
            if request.POST['Order']:
                while True:
                    O_id = random.randint(0,9999999)
                    print(O_id)
                    try:
                        abc = Orders.objects.get(o_id = O_id)
                    except:
                        try:
                            mids = request.POST.getlist('prod_id')
                            mrqts = request.POST.getlist('qt')
                            for i in range(len(mids)):
                                new_mdord = Med_per_ord(o_id = O_id, m_id = mids[i], m_qt = mrqts[i], U_name = request.user.username)
                                new_mdord.save()
                                Cart.objects.filter(Username=request.user).get(p_id=mids[i]).delete()
                            new_ord = Orders(o_id = O_id, UserName = request.user.username ,Date = date.today(), 
                                Time = datetime.now().strftime("%H:%M:%S"), Address = request.POST['Address'])
                            new_ord.save()
                            messages.success(request, 'Order placed successfully.')
                            return redirect('/shopping')
                        except Exception as e:
                            print(type(e),e.args)
                            break
        except MultiValueDictKeyError:
            print("Order: ", MultiValueDictKeyError)

    pds = Cart.objects.filter(Username=request.user.username)
    for pd in pds:
        temp = vars(M_remedy.objects.get(pk=pd.p_id))
        temp['cartid'] = pd.pk
        temp['qprice'] = temp['Price'] * pd.quantity
        temp['quant'] = pd.quantity
        crt.append(temp)
    return render(request, 'user/Cart.html', {'Cart': crt, 'prdno': len(pds)})


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
                new_blog = Blogs(Title=title, Type=Btype,
                                 Content=content, Date=dt, file=File)
                new_blog.save()
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)
        # view

    Bls = Blogs.objects.all().order_by(jinja['bl_sort'])
    return render(request, 'user/our_blogs.html', {'Bls': Bls})

# -----------------------------ADMIN SIDE---------------------------


def dashboard(request):
    if request.user.is_superuser:
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
            all_data['apts_ct'] = round((len(CApts) / len(Apts))*100, 2)
        except:
            all_data['apts_ct'] = 0
        try:
            all_data['ords_ct'] = round((len(COrds) / len(Ords))*100, 2)
        except:
            all_data['ords_ct'] = 0

        print(all_data)
        return render(request, 'admin/Dashboard.html', {'data': all_data})
    else:
        return redirect('/')


def patients(request):
    new_pts = []
    if request.method == 'POST':
        print(request.POST)
        try:
            if request.POST['sort']:
                jinja['pt_sort'] = request.POST['sort']
        except:
            pass
        try:
            if request.POST['search']:
                if request.POST['srch'] == '1':
                    if (jinja['pt_sort'] == 'first_name' or jinja['pt_sort'] == 'email'):
                        Pts = User.objects.all().order_by(jinja['pt_sort'])
                    else:
                        Pts = Users.objects.all().order_by(jinja['pt_sort'])
                    string = request.POST['search'].lower()
                    for Pt in Pts:
                        if (jinja['pt_sort'] == 'first_name' or jinja['pt_sort'] == 'email'):
                            Pt_ext = Users.objects.get(UserName=Pt.username)
                            strs = (Pt.first_name+" " +
                                    Pt_ext.Middle_name+" " + Pt.last_name)
                        else:
                            Pt_ext = User.objects.get(username=Pt.UserName)
                            strs = (Pt_ext.first_name+" " +
                                    Pt.Middle_name+" " + Pt_ext.last_name)
                        strs = strs.lower()
                        print(string, strs)
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
                    Pts = User.objects.filter(
                        email__contains=request.POST['search'])
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
                    Pts = Users.objects.filter(
                        Phone_No__contains=request.POST['search'])
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
            print("Search User: ", MultiValueDictKeyError)

        try:
            if request.POST['submit']:
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
                messages.success(request, 'User is created.')
            else:
                messages.error(request, 'User is not created.')
        except MultiValueDictKeyError:
            print("Add User: ", MultiValueDictKeyError)

        # remove patient code
        try:
            if request.POST['remove']:
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
                messages.error(request, 'User is removed.')
            else:
                messages.error(request, 'User is not removed.')
        except MultiValueDictKeyError:
            print("Remove User: ", MultiValueDictKeyError)

        # appintment booking
        try:
            if request.POST['book']:
                print(request.POST['book'])
                dt, slot = getNextAvailableSlot()
                print(dt, slot)
                if dt != null and slot != null:
                    new_apt = Appointments(
                        U_id=request.POST['book'], Date=dt, TimeSlot=slot)
                    new_apt.save()
                    pass
                else:
                    messages.warning(
                        request, 'Slot is not available for next 5 days.')
                    pass
                messages.success(request, 'Appintment is Booked.')
                pass
            else:
                messages.error(request, 'Appintment is not Booked.')
        except MultiValueDictKeyError:
            print("Book Appointment: ", MultiValueDictKeyError)

    if (jinja['pt_sort'] == 'first_name' or jinja['pt_sort'] == 'email'):
        Pts = User.objects.all().order_by(jinja['pt_sort'])
    else:
        Pts = Users.objects.all().order_by(jinja['pt_sort'])
    for Pt in Pts:
        id = Pt.pk
        if (jinja['pt_sort'] == 'first_name' or jinja['pt_sort'] == 'email'):
            Pt_ext = Users.objects.get(UserName=Pt.username)
        else:
            Pt_ext = User.objects.get(username=Pt.UserName)
        if Pt_ext:
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
            new_pt['id'] = id
            new_pts.append(new_pt)
    print("sorting by ", jinja['pt_sort'], new_pts)
    print(new_pts)
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
                        string = request.POST['search'].lower()
                        Pt = Users.objects.get(id=Apt.U_id)
                        Pt_exts = User.objects.filter(username=Pt.UserName)
                        for Pt_ext in Pt_exts:
                            strs = (Pt_ext.first_name+" " +
                                    Pt.Middle_name+" " + Pt_ext.last_name)
                            strs = strs.lower()
                            print(string, strs)
                            if string in strs:
                                new_apt = vars(Apt)
                                new_apt['full_name'] = Pt_ext.first_name+' ' + \
                                    Pt.Middle_name+' '+Pt_ext.last_name
                                new_apt['email'] = Pt_ext.email
                                new_apt['phno'] = Pt.Phone_No
                                new_apt['age'] = Pt.Age
                                new_apt['gender'] = Pt.Gender
                                new_apt.pop('_state')
                                new_apts.append(new_apt)
                    return render(request, 'admin/appointments.html', {'Apts': new_apts})
                if request.POST['srch'] == '2':
                    try:
                        Apt = Appointments.objects.get(
                            pk=request.POST['search'])
                        Pt = Users.objects.get(pk=Apt.U_id)
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
                    mail = str(request.POST['search'])
                    Pts = User.objects.filter(email__contains=mail.lower())
                    for Pt in Pts:
                        Pt_ext = Users.objects.get(UserName=Pt.username)
                        Apts = Appointments.objects.filter(U_id=Pt_ext.pk)
                        for Apt in Apts:
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
                    Pts = Users.objects.filter(
                        Phone_No__contains=request.POST['search'])
                    for Pt in Pts:
                        Pt_ext = User.objects.get(username=Pt.UserName)
                        Apts = Appointments.objects.filter(U_id=Pt.pk)
                        for Apt in Apts:
                            new_apt = vars(Apt)
                            new_apt['full_name'] = Pt_ext.first_name+' ' + \
                                Pt.Middle_name+' '+Pt_ext.last_name
                            new_apt['email'] = Pt_ext.email
                            new_apt['phno'] = Pt.Phone_No
                            new_apt['age'] = Pt.Age
                            new_apt['gender'] = Pt.Gender
                            new_apt.pop('_state')
                            new_apts.append(new_apt)
                    return render(request, 'admin/appointments.html', {'Apts': new_apts})
                if request.POST['srch'] == '5':
                    Pts = Users.objects.filter(Age__gte=request.POST['search'])
                    for Pt in Pts:
                        Pt_ext = User.objects.get(username=Pt.UserName)
                        Apts = Appointments.objects.filter(U_id=Pt.pk)
                        for Apt in Apts:
                            new_apt = vars(Apt)
                            new_apt['full_name'] = Pt_ext.first_name+' ' + \
                                Pt.Middle_name+' '+Pt_ext.last_name
                            new_apt['email'] = Pt_ext.email
                            new_apt['phno'] = Pt.Phone_No
                            new_apt['age'] = Pt.Age
                            new_apt['gender'] = Pt.Gender
                            new_apt.pop('_state')
                            new_apts.append(new_apt)
                        print(new_apts)
                    return render(request, 'admin/appointments.html', {'Apts': new_apts})
        except MultiValueDictKeyError:
            print('searching', MultiValueDictKeyError)
        # reschedule
        try:
            if request.POST['reschedule']:
                Aid = request.POST['apptID']
                Appnt = request.POST['appnt']
                Day = int(request.POST['day'])-1
                print(request.POST, "\n", Day)
                # appintment reschedule code
                if Day == 2:
                    Date = request.POST['date']
                    if getAvailableSlot(Date, Appnt):
                        new_apt = Appointments.objects.get(id=Aid)
                        new_apt.Date = Date
                        new_apt.TimeSlot = Appnt
                        new_apt.Status_R = True
                        new_apt.save()
                        messages.success(
                            request, 'Appointment slot is booked.')
                    else:
                        messages.warning(
                            request, 'Appointment slot is not available.')
                else:
                    if Day == 1:
                        Date = datetime.now() + timedelta(1)
                    else:
                        Date = datetime.now()
                    Date = Date.strftime('%Y-%m-%d')
                    print(Date)
                    if getAvailableSlot(Date, Appnt):
                        new_apt = Appointments.objects.get(id=Aid)
                        new_apt.Date = Date
                        new_apt.TimeSlot = Appnt
                        new_apt.Status_R = True
                        new_apt.save()
                        messages.success(
                            request, 'Appointment slot is booked.')
                    else:
                        messages.error(
                            request, 'Appointment slot is not available.')
            else:
                messages.error(request, 'Appointment slot is not resheduled.')
        except MultiValueDictKeyError:
            print("Appointment Reschedule: ", MultiValueDictKeyError)

        # prescribe
        try:
            if request.POST['prescribe']:
                Pid = request.POST['P_apptID']
                Presc = request.POST['Description']
                # add prescription code
                new_apt = Appointments.objects.get(id=Pid)
                new_apt.P_med = Presc
                new_apt.Status_A = True
                new_apt.save()
                messages.success(
                    request, 'Remedies are prescribed and Appointment is attended.')
            else:
                messages.error(request, 'Remedies are not prescribed.')
        except MultiValueDictKeyError:
            print("Appointment Prescribe: ", MultiValueDictKeyError)

        # remove
        try:
            if request.POST['remove']:
                # remove appintment code
                # print(request.POST['remove'])
                Appointments.objects.get(id=request.POST['remove']).delete()
                messages.error(request, 'Appointment is deleted.')
            else:
                messages.error(request, 'Appointment is not deleted.')
        except MultiValueDictKeyError:
            print("Appointment Remove: ", MultiValueDictKeyError)

    # view
    Apts = Appointments.objects.all().order_by(jinja['apt_sort'])
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
    # print(new_apts)
    # print(Apts)
    return render(request, 'admin/appointments.html', {'Apts': new_apts})


def M_remedies(request):

    if request.method == 'POST':
        print(request.POST)
        try:
            if request.POST['sort']:
                jinja['mr_sort'] = request.POST['sort']
                print('hello', jinja['mr_sort'])
        except:
            pass
        try:
            if request.POST['search']:
                if request.POST['srch'] == '1':
                    MRs = M_remedy.objects.filter(
                        Name__contains=request.POST['search'])
                    return render(request, 'admin/M_remedies.html', {'MRs': MRs})
                if request.POST['srch'] == '2':
                    try:
                        MRs = M_remedy.objects.filter(
                            id=request.POST['search'])
                        return render(request, 'admin/M_remedies.html', {'MRs': MRs})
                    except:
                        MRs = []
                        return render(request, 'admin/M_remedies.html', {'MRs': MRs})
                if request.POST['srch'] == '3':
                    MRs = M_remedy.objects.filter(
                        Price__gte=int(request.POST['search']))
                    return render(request, 'admin/M_remedies.html', {'MRs': MRs})
        except MultiValueDictKeyError:
            print(MultiValueDictKeyError)
        try:
            m_id = request.POST['m_id']
            name = request.POST['name']
            category = request.POST['category']
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
                update_med = M_remedy.objects.get(id=m_id)
                update_med.Name = name
                update_med.Category = category
                update_med.Desc = description
                update_med.Content = contents
                update_med.Quantity = quantity
                update_med.Price = price
                update_med.Img = picture
                update_med.save()
                messages.success(request, 'Medicine Remedy is updated.')
                pass
            else:
                messages.error(request, 'Medicine Remedy is not updated.')
            
            if request.POST['submit'] == 'Create':
                # add medicine code
                new_med = M_remedy(Name=name, Desc=description, Content=contents,
                                    Quantity=quantity, Price=price, Img=picture)
                new_med.save()
                messages.success(request, 'Medicine Remedy is inserted.')
            else:
                messages.error(request, 'Medicine Remedy is not inserted.')
        except MultiValueDictKeyError:
            print("Update and Add medicine: ", MultiValueDictKeyError)

        try:
            if request.POST['remove']:
                # remove medicine code
                mr = M_remedy.objects.get(id=request.POST['remove'])
                mds = Med_per_ord.objects.filter(m_id=mr.pk)
                for md in mds:
                    md.m_id = -1
                    md.save()
                mr.delete()
                messages.error(request, 'Medicine Remedy is deleted.')
            else:
                messages.error(request, 'Medicine Remedy is not deleted.')
        except MultiValueDictKeyError:
            print("Remove medicine: ", MultiValueDictKeyError)

    # view
    MRs = M_remedy.objects.all().order_by(jinja['mr_sort'])
    print('order by :', jinja['mr_sort'], MRs)
    # print(MRs)
    return render(request, 'admin/M_remedies.html', {'MRs': MRs})


def H_remedies(request):
    if request.method == 'POST':
        print(request.POST)
        try:
            if request.POST['sort']:
                jinja['hr_sort'] = request.POST['sort']
                print('hello', jinja['hr_sort'])
        except:
            pass
        try:
            if request.POST['search']:
                if request.POST['srch'] == '1':
                    HRs = H_remedy.objects.filter(
                        Name__contains=request.POST['search'])
                    return render(request, 'admin/H_remedies.html', {'HRs': HRs})
                if request.POST['srch'] == '2':
                    try:
                        HRs = H_remedy.objects.filter(
                            id=request.POST['search'])
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
                messages.success(request, 'Home Remedy is updated.')
                pass
            else:
                messages.error(request, 'Home Remedy is not updated.')
            if request.POST['submit'] == 'Create':
                # add remedy code
                new_hmed = H_remedy(Name=title, Desc=desc,
                                    Accessories=acce, Img=picture)
                new_hmed.save()
                messages.success(request, 'Home Remedy is inserted.')
            else:
                messages.error(request, 'Home Remedy is not inserted.')
        except MultiValueDictKeyError:
            print("update and add home med: ", MultiValueDictKeyError)

        try:
            if request.POST['remove']:
                # remove remedy code
                H_remedy.objects.filter(id=request.POST['remove']).delete()
                messages.success(request, 'Home Remedy not deleted.')
                pass
            else:
                messages.error(request, 'Home Remedy is not deleted.')
        except MultiValueDictKeyError:
            print("remove home med: ", MultiValueDictKeyError)

    # view
    HRs = H_remedy.objects.all().order_by(jinja['hr_sort'])
    print('order by :', jinja['hr_sort'], HRs)

    return render(request, 'admin/H_remedies.html', {'HRs': HRs})


def blogs(request):
    type = ["BLOG", "IMAGE", "VIDEO"]
    if request.method == 'POST':
        type = ["BLOG", "IMAGE", "VIDEO"]
        print(request.POST)
        print(request.FILES)
        try:
            if request.POST['sort']:
                jinja['bl_sort'] = request.POST['sort']
                print('hello', jinja['bl_sort'])
        except:
            pass
        try:
            if request.POST['search']:
                # if request.POST['srch'] == '1':
                Bls = Blogs.objects.filter(
                    Title__contains=request.POST['search'])
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
            dt = date.today()
            if Btype == 'BLOG':
                content = request.POST['content']
            else:
                try:
                    File = request.FILES['inFile']
                except:
                    File = request.POST['ImgURL']
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
                messages.success(request, 'Blog is edited.')
                pass
            else:
                messages.error(request, 'Blog is not edited.')
            if request.POST['submit'] == 'Create':
                # add blog code
                new_blog = Blogs(Title=title, Type=Btype,
                                 Content=content, Date=dt, file=File)
                new_blog.save()
                messages.success(request, 'Blog is posted.')
            else:
                messages.error(request, 'Blog is not posted.')
        except MultiValueDictKeyError:
            print("update and add blog: ", MultiValueDictKeyError)

        try:
            if request.POST['remove']:
                # remove blog code
                Blogs.objects.get(id=request.POST['remove']).delete()
                messages.error(request, 'Blog is deleted.')
                pass
            else:
                messages.error(request, 'Blog is not deleted.')
        except MultiValueDictKeyError:
            print("remove blog: ", MultiValueDictKeyError)

    # view
    Bls = Blogs.objects.all().order_by(jinja['bl_sort'])
    print('order by :', jinja['bl_sort'], Bls)
    return render(request, 'admin/blogs.html', {'Bls': Bls})


def orders(request):

    new_ords = []
    if request.POST:
        print(request.POST)
        try:
            if request.POST['sort']:
                jinja['ord_sort'] = request.POST['sort']
                print('hello', jinja['ord_sort'])
        except:
            pass
        # search
        try:
            if request.POST['search']:
                if request.POST['srch'] == '1':
                    string = request.POST['search'].lower()
                    Pts = Users.objects.all()
                    for Pt in Pts:
                        Pt_ext = User.objects.get(username=Pt.UserName)
                        strs = (Pt_ext.first_name+" "+Pt.Middle_name +
                                " " + Pt_ext.last_name).lower()
                        print(string, strs)
                        if string in strs:
                            Ords = Orders.objects.all()
                            for Ord in Ords:
                                new_ord = vars(Ord)
                                new_ord.pop('_state')
                                new_ord['full_name'] = Pt_ext.first_name + \
                                    " "+Pt.Middle_name+" " + Pt_ext.last_name
                                new_ord['email'] = Pt_ext.email
                                new_ord['phno'] = Pt.Phone_No
                                Pids = Med_per_ord.objects.filter(
                                    o_id=Ord.o_id)
                                Prds = []
                                for Pid in Pids:
                                    temp = {}
                                    Prd = M_remedy.objects.get(id=Pid.m_id)
                                    temp['name'] = Prd.Name
                                    temp['price'] = Prd.Price
                                    temp['quantity'] = 0
                                    temp['m_id'] = Pid.m_id
                                    temp['m_name'] = Pid.m_name
                                    Prds.append(temp)
                                new_ord['products'] = Prds
                                new_ords.append(new_ord)
                        print(new_ords)
                    return render(request, 'admin/Orders.html', {'orders': new_ords})
                if request.POST['srch'] == '2':
                    try:
                        Ord = Orders.objects.get(o_id=request.POST['search'])
                        Pt = Users.objects.get(UserName=Ord.UserName)
                        Pt_ext = User.objects.get(username=Pt.UserName)
                        new_ord = vars(Ord)
                        new_ord.pop('_state')
                        new_ord['full_name'] = Pt_ext.first_name + \
                            ' '+Pt.Middle_name+' '+Pt_ext.last_name
                        new_ord['email'] = Pt_ext.email
                        new_ord['phno'] = Pt.Phone_No
                        Pids = Med_per_ord.objects.filter(o_id=Ord.o_id)
                        Prds = []
                        for Pid in Pids:
                            temp = {}
                            Prd = M_remedy.objects.get(id=Pid.m_id)
                            temp['name'] = Prd.Name
                            temp['price'] = Prd.Price
                            temp['quantity'] = 0
                            temp['m_id'] = Pid.m_id
                            temp['m_name'] = Pid.m_name
                            Prds.append(temp)
                        new_ord['products'] = Prds
                        new_ords.append(new_ord)
                        return render(request, 'admin/Orders.html', {'orders': new_ords})
                    except:
                        return render(request, 'admin/Orders.html', {'orders': new_ords})
                if request.POST['srch'] == '3':
                    Pts = User.objects.filter(
                        email__contains=request.POST['search'])
                    for Pt in Pts:
                        Pt_ext = Users.objects.get(UserName=Pt.username)
                        Ords = Users.objects.filter(UserName=Pt_ext.UserName)
                        for Ord in Ords:
                            new_ord = vars(Ord)
                            new_ord.pop('_state')
                            new_ord['full_name'] = Pt.first_name+' ' + \
                                Pt_ext.Middle_name+' '+Pt.last_name
                            new_ord['email'] = Pt.email
                            new_ord['phno'] = Pt_ext.Phone_No
                            Pids = Med_per_ord.objects.filter(o_id=Ord.o_id)
                            Prds = []
                            for Pid in Pids:
                                temp = {}
                                Prd = M_remedy.objects.get(id=Pid.m_id)
                                temp['name'] = Prd.Name
                                temp['price'] = Prd.Price
                                temp['quantity'] = 0
                                temp['m_id'] = Pid.m_id
                                temp['m_name'] = Pid.m_name
                                Prds.append(temp)
                            new_ord['products'] = Prds
                            new_ords.append(new_ord)
                    return render(request, 'admin/Orders.html', {'orders': new_ords})
                if request.POST['srch'] == '4':
                    Pts = Users.objects.filter(
                        email__contains=request.POST['search'])
                    for Pt in Pts:
                        Pt_ext = User.objects.get(username=Pt.UserName)
                        Ords = Users.objects.filter(UserName=Pt_ext.username)
                        for Ord in Ords:
                            new_ord = vars(Ord)
                            new_ord.pop('_state')
                            new_ord['full_name'] = Pt_ext.first_name + \
                                ' ' + Pt.Middle_name+' '+Pt_ext.last_name
                            new_ord['email'] = Pt_ext.email
                            new_ord['phno'] = Pt.Phone_No
                            Pids = Med_per_ord.objects.filter(o_id=Ord.o_id)
                            Prds = []
                            for Pid in Pids:
                                temp = {}
                                Prd = M_remedy.objects.get(id=Pid.m_id)
                                temp['name'] = Prd.Name
                                temp['price'] = Prd.Price
                                temp['quantity'] = 0
                                temp['m_id'] = Pid.m_id
                                temp['m_name'] = Pid.m_name
                                Prds.append(temp)
                            new_ord['products'] = Prds
                            new_ords.append(new_ord)
                    return render(request, 'admin/Orders.html', {'orders': new_ords})
                if request.POST['srch'] == '5':
                    Ords = Orders.objects.all()
                    for Ord in Ords:
                        new_ord = vars(Ord)
                        new_ord.pop('_state')
                        patient = User.objects.get(username=Ord.UserName)
                        patient_ext = Users.objects.get(
                            UserName=patient.username)
                        new_ord['full_name'] = patient.first_name+' ' + \
                            patient_ext.Middle_name+' '+patient.last_name
                        new_ord['email'] = patient.email
                        new_ord['phno'] = patient_ext.Phone_No
                        Pids = Med_per_ord.objects.filter(
                            m_name__contains=request.POST['search'])
                        Prds = []
                        for Pid in Pids:
                            temp = {}
                            Prd = M_remedy.objects.filter(id=Pid.m_id)
                            temp['name'] = Prd.Name
                            temp['price'] = Prd.Price
                            temp['quantity'] = 0
                            temp['m_id'] = Pid.m_id
                            temp['m_name'] = Pid.m_name
                            Prds.append(temp)
                        new_ord['products'] = Prds
                        new_ords.append(new_ord)
                    return render(request, 'admin/Orders.html', {'orders': new_ords})
        except MultiValueDictKeyError:
            print('Searching', MultiValueDictKeyError)
        # remove
        try:
            if request.POST['remove']:
                # remove order code
                ord = Orders.objects.get(id=request.POST['remove'])
                mds = Med_per_ord.objects.filter(o_id=ord.o_id)
                for md in mds:
                    md.delete()
                ord.delete()
                messages.error(request, 'Oreder is deleted.')
            else:
                messages.error(request, 'Order is not deleted.')
        except MultiValueDictKeyError:
            print('remove', MultiValueDictKeyError)

    # view
    Ords = Orders.objects.all().order_by(jinja['ord_sort'])
    for Ord in Ords:
        new_ord = vars(Ord)
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
            temp['name'] = Prd.Name
            temp['price'] = Prd.Price
            temp['quantity'] = 0
            temp['m_id'] = Pid.m_id
            temp['m_name'] = Pid.m_name
            Prds.append(temp)
        new_ord['products'] = Prds
        new_ords.append(new_ord)
    return render(request, 'admin/Orders.html', {'orders': new_ords})


def A_profile(request):
    if request.POST:
        print(request.POST)
        print(request.FILES)
        try:
            if request.POST['submit']:
                usr = User.objects.get(id=request.POST['patient_id'])
                usr_ext = Users.objects.get(UserName=usr.username)
                usr.first_name = request.POST['Fname']
                usr_ext.Middle_name = request.POST['Mname']
                usr.last_name = request.POST['Lname']
                usr.email = request.POST['Email']
                usr_ext.Phone_No = request.POST['Phone']
                usr_ext.Gender = getGender(request.POST['Gender'])
                usr_ext.Age = request.POST['Age']
                try:
                    usr_ext.P_Prakruti, usr_ext.S_Prakruti = getPrakruti(
                        request.POST['Prakruti'])
                except:
                    pass
                try:
                    print('file', request.FILES['inFile'])
                    usr_ext.Img = request.FILES['inFile']
                except:
                    pass
                usr.save()
                usr_ext.save()
                print("____________________________________")
                print('user updated successfully')
        except:
            pass

        usr = User.objects.get(id=request.POST['patient_id'])
        usr_ext = Users.objects.get(UserName=usr.username)
        Usrs = vars(usr)
        Usrs.update(vars(usr_ext))
        Usrs['admin'] = 0
        Usrs['appnts'] = Appointments.objects.filter(U_id=usr_ext.pk)
        try:
            if request.POST['search']:
                Usrs['appnts'] = Appointments.objects.filter(
                    id=request.POST['search'])
        except:
            Usrs['appnts'] = Appointments.objects.filter(U_id=usr_ext.pk)
        # print(Usrs)
        return render(request, 'admin/A_profile.html', {'users': Usrs})
    usr = User.objects.get(username=request.user.username)
    usr_ext = Users.objects.get(UserName=usr.username)
    Usrs = vars(usr)
    Usrs.update(vars(usr_ext))
    Usrs['admin'] = 1
    return render(request, 'admin/A_profile.html', {'users': Usrs})


def dataInsert(request):
    # quetions = [
    #     {'Q': 'Q1. What is your Body Build Type?',
    #      'C1': 'Lean/slim', 'C2': 'Medium', 'C3': 'Stout/heavy build'},
    #     {'Q': 'Q2. What is your Face size?', 'C1': 'Small',
    #      'C2': 'Medium', 'C3': 'Big'},
    #     {'Q': 'Q3. What is your face color?', 'C1': 'Brown',
    #      'C2': 'Reddish white', 'C3': 'Fair'},
    #     {'Q': 'Q4. What is your body capacity?', 'C1': 'Poor',
    #      'C2': 'Average', 'C3': 'Incredible'},
    #     {'Q': 'Q5. What is your nature of behavior?',
    #      'C1': 'Playful', 'C2': 'Aggressive', 'C3': 'Calm minded'},
    #     {'Q': 'Q6. What is your favorite season?',
    #      'C1': 'Spring', 'C2': 'Winter', 'C3': 'Summer'},
    #     {'Q': 'Q7. What is your favorite dishes?',
    #      'C1': 'Sweet salty and sour', 'C2': 'Spicy sweet', 'C3': 'Bitter spicy hot'},
    #     {'Q': 'Q8. How much is your Grasping power?',
    #      'C1': 'poor', 'C2': 'Sharp', 'C3': 'Average/ Good'},
    #     {'Q': 'Q9. How is your memorizing ability?',
    #      'C1': 'Observant but forgot', 'C2': 'Sharp and clear', 'C3': 'Average/ good'},
    #     {'Q': 'Q10. How is your Digestion power?',
    #      'C1': 'Sometimes less, sometimes better', 'C2': 'Quick digestion, frequent hunger', 'C3': 'Late digestion'},
    #     {'Q': 'Q11. What is your diet capacity?',
    #      'C1': 'sometimes poor, sometimes higher', 'C2': 'Medium', 'C3': 'Heavier'},
    #     {'Q': 'Q12. What is your body color?',
    #      'C1': 'Brownish', 'C2': 'fair, dusky', 'C3': 'Reddish white'},
    #     {'Q': 'Q13. What is your hair type?', 'C1': 'Dry, fally',
    #      'C2': 'Faster ripping', 'C3': 'Thick, Smooth, Long'},
    #     {'Q': 'Q14. What is your Type of your Eyes?',
    #      'C1': 'Dry, small', 'C2': 'Shiny, Gray-green', 'C3': 'Big, Lazy, thick eyelids'},
    #     {'Q': 'Q15. What is your Type of teeth?',
    #      'C1': 'Uneven, Big', 'C2': 'Medium, Pretty', 'C3': 'Even, tender'},
    #     {'Q': 'Q16. What is your Stool instinct?',
    #      'C1': 'Dry, Tight', 'C2': 'Tender, Spread out', 'C3': 'Excessive, Flimsy'},
    #     {'Q': 'Q17. What is your sweat instinct?',
    #      'C1': 'Poor', 'C2': 'Excess, Smelly', 'C3': 'Medium'},
    #     {'Q': 'Q18. How are your Joints?', 'C1': 'Smaller, Hurting, Noisy',
    #      'C2': 'Medium, No Noise', 'C3': 'Bigger, No Noise'},
    #     {'Q': 'Q19. How is your sleep?', 'C1': 'Less, Restless',
    #      'C2': 'Less, but Restful', 'C3': 'Deep sleep'},
    #     {'Q': 'Q20. How are your dreams?', 'C1': 'Scary',
    #      'C2': 'Aggressive, Violent', 'C3': 'Peaceful, Lake, River, Sea'},
    #     {'Q': 'Q21. How is your skin Type?', 'C1': 'Dry, Rough',
    #      'C2': 'Bright, Glorious', 'C3': 'Tender, Soft'},
    #     {'Q': 'Q22. How is Your Menstruation (For woman only)?',
    #      'C1': 'Less flow, More abdominal pain', 'C2': 'Heavy flow', 'C3': 'Moderate flow'},
    #     {'Q': 'Q23. How is your Pulse?', 'C1': 'Snakelike, Feebi',
    #      'C2': 'Froglike , Faster', 'C3': 'Gentle, Steady'},
    # ]

    # quetions = [
    #     {'Q': 'Do you feel weakness with body cramp',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'vata'},
    #     {'Q': 'Not having interest in daily activities',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'vata'},
    #     {'Q': 'Abdominal discomfort bloating gases flatulance',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'vata'},
    #     {'Q': 'Do you having blackish discoloration of body parts',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'vata'},
    #     {'Q': 'Do you have constipation', 'C1': 'Yes',
    #         'C2': 'No', 'prakruti': 'vata'},
    #     {'Q': 'Do you have sleep disturbance / irregular sleep pattern',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'vata'},
    #     {'Q': 'Do you feel weakness & reduced strenght',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'vata'},
    #     {'Q': 'Do you have rough skin or scaling on skin',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'vata'},
    #     {'Q': 'Do you feel body pain or joint pain',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'vata'},
    #     {'Q': 'Do you feel gargling sound in bowels',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'vata'},
    #     {'Q': 'Do you often ffeel indigestion, sluggish digestion',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'pitta'},
    #     {'Q': 'Do you feeling lact of body luster appearance',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'pitta'},
    #     {'Q': 'Do you often feeling burning sensation thurst or hunger',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'pitta'},
    #     {'Q': 'Does your urine,stool,skin,eyes are dark yellow coloured',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'pitta'},
    #     {'Q': 'Do you feel excessive heat & sweating',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'pitta'},
    #     {'Q': 'Do you have reddish discolouration on skin',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'pitta'},
    #     {'Q': 'Do you often feel heart burn,acidic bleching',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'pitta'},
    #     {'Q': 'Do you feel heaviness in body',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'kapha'},
    #     {'Q': 'Do you feel lazy or litharqic often',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'kapha'},
    #     {'Q': 'Do you have common cold', 'C1': 'Yes',
    #         'C2': 'No', 'prakruti': 'kapha'},
    #     {'Q': 'Do you having exessive salivation',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'kapha'},
    #     {'Q': 'Do you have feeling of sleep all the time',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'kapha'},
    #     {'Q': 'Do you have vomiting or indigestion',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'kapha'},
    #     {'Q': 'Feeling as if body covered by a wet or damp cloth',
    #         'C1': 'Yes', 'C2': 'No', 'prakruti': 'kapha'},
    #     {'Q': 'Do you have cough', 'C1': 'Yes', 'C2': 'No', 'prakruti': 'kapha'},
    # ]

    # for q in quetions:
    #     print(q.get('Q'))
    #     print(q.get('C1'), q.get('C2'), q.get('prakruti'))
    #     med = Complaint_Quetions(que=q.get('Q'), choice1=q.get(
    #         'C1'), choice2=q.get('C2'), prakruti=q.get('prakruti'))
    #     med.save()
    return render(request, 'index.html')