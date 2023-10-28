# from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse
from ..models import Users, Appointments, M_remedy, Blogs, Orders, Prakruti_Quetions, Med_per_ord, Cart, Complaint_Quetions, Prakruti_Quetions_Ans
from django.contrib.auth.models import User, auth
from django.contrib import messages

from django.utils.datastructures import MultiValueDictKeyError
import random
from datetime import date, datetime

from .sharedController import jinja, getGender, getPrakruti


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
        # ip  = []
        # for i in range(1, 24):
        #     ip.append(request.POST[str(i)])
        # pr,sc = rcmd(ip)

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
                usr.age = age
                usr.ans1 = request.POST['1']
                usr.ans2 = request.POST['2']
                usr.ans3 = request.POST['3']
                usr.ans4 = request.POST['4']
                usr.ans5 = request.POST['5']
                usr.ans6 = request.POST['6']
                usr.ans7 = request.POST['7']
                usr.ans8 = request.POST['8']
                usr.ans9 = request.POST['9']
                usr.ans10 = request.POST['10']
                usr.ans11 = request.POST['11']
                usr.ans12 = request.POST['12']
                usr.ans13 = request.POST['13']
                usr.ans14 = request.POST['14']
                usr.ans15 = request.POST['15']
                usr.ans16 = request.POST['16']
                usr.ans17 = request.POST['17']
                usr.ans18 = request.POST['18']
                usr.ans19 = request.POST['19']
                usr.ans20 = request.POST['20']
                usr.ans21 = request.POST['21']
                usr.ans22 = request.POST['22']
                usr.ans23 = request.POST['23']
                usr.save()
            except:
                ans = Prakruti_Quetions_Ans(u_id=request.user.id, age=age, ans1=request.POST['1'], ans2=request.POST['2'],
                                            ans3=request.POST['3'], ans4=request.POST['4'], ans5=request.POST['5'],
                                            ans6=request.POST['6'], ans7=request.POST['7'], ans8=request.POST['8'],
                                            ans9=request.POST['9'], ans10=request.POST['10'], ans11=request.POST['11'],
                                            ans12=request.POST['12'], ans13=request.POST['13'], ans14=request.POST['14'],
                                            ans15=request.POST['15'], ans16=request.POST['16'], ans17=request.POST['17'],
                                            ans18=request.POST['18'], ans19=request.POST['19'], ans20=request.POST['20'],
                                            ans21=request.POST['21'], ans22=request.POST['22'], ans23=request.POST['23'])
                ans.save()
        print(prakruti, prakrutict['vata'],
              prakrutict['pitta'], prakrutict['kapha'])
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
    user = Users.objects.get(UserName=request.user)
    prakruti['p'] = user.P_Prakruti.capitalize()
    prakruti['s'] = user.S_Prakruti.capitalize()
    prk = prakruti['p'] + prakruti['s']
    prakruti['d'] = discription[prk]
    print("prakruti:", prakruti)

    # fetching Questions
    Ques = Complaint_Quetions.objects.filter(prakruti=user.P_Prakruti)
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
                T = 0
                for i in range(1, recc + 1):
                    if request.POST[str(i)]:
                        T += 1
                gen = Users.objects.get(UserName=request.user).Gender
                if gen == 'Male':
                    exc = M_remedy.objects.filter(Category='MEN\'S HEALTH')
                elif gen == 'Female':
                    exc = M_remedy.objects.filter(Category='WOMEN\'S HEALTH')
                else:
                    exc = M_remedy.objects.filter(Category='Skincare')
                print(exc)
                recm = M_remedy.objects.all().order_by('?').difference(exc)
                if recc/2 >= T:
                    recm = recm[:T]
                else:
                    recm = recm[:recc-4]
                other = M_remedy.objects.all().difference(recm)
                print(recm, "\n", other)
                jinja['rcmd'] = recm
                print("out reccc")
                return render(request, 'user/Shopping.html', {'other': other, "recm": recm, "prakruti": prakruti})
        except MultiValueDictKeyError:
            print("Recommend: ", MultiValueDictKeyError)

        try:
            if request.POST['buy_now']:
                cts = Cart.objects.filter(Username=request.user).filter(
                    p_id=request.POST['buy_now'])
                for ct in cts:
                    print("olditem", ct, ct.quantity, ct.p_id)
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
                    print('olditem', ct, ct.quantity, ct.p_id)
                    ct.save()
                    print("item added to cart of id : ", request.POST['cart'])
                    messages.success(request, 'Item added to cart.')
                    try:
                        pds = M_remedy.objects.all().difference(jinja['rcmd'])
                    except:
                        pds = M_remedy.objects.all()
                    return render(request, 'user/Shopping.html', {'other': pds, "recm": jinja['rcmd'], "prakruti": prakruti})
                new_cart = Cart(Username=request.user,
                                p_id=request.POST['cart'], quantity=1)
                new_cart.save()
                messages.success(request, 'Item added to cart.')
                print("new item added to cart of id : ", request.POST['cart'])
        except MultiValueDictKeyError:
            print("Cart: ", MultiValueDictKeyError)

        try:
            if request.POST['category']:
                try:
                    category = request.POST.getlist('category')
                    pds = M_remedy.objects.filter(Category="")
                    for cat in category:
                        pds = pds.union(M_remedy.objects.filter(Category=cat))
                    try:
                        pds = pds.difference(jinja['rcmd'])
                    except:
                        pass
                    print(pds)
                    return render(request, 'user/Shopping.html', {'other': pds, "recm": jinja['rcmd'], "prakruti": prakruti})
                except:
                    pass
        except:
            print("Categorize: ", MultiValueDictKeyError)

    try:
        pds = M_remedy.objects.all().difference(jinja['rcmd'])
    except:
        pds = M_remedy.objects.all()
    return render(request, 'user/Shopping.html', {'other': pds, "recm": jinja['rcmd'], "prakruti": prakruti})


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
                    usr.P_Prakruti, usr.S_Prakruti = getPrakruti(
                        request.POST['Prakruti'])
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
                    O_id = random.randint(0, 9999999)
                    print(O_id)
                    try:
                        tmp = Orders.objects.get(o_id=O_id)
                    except:
                        try:
                            mids = request.POST.getlist('prod_id')
                            mrqts = request.POST.getlist('qt')
                            for i in range(len(mids)):
                                new_mdord = Med_per_ord(
                                    o_id=O_id, m_id=mids[i], m_qt=mrqts[i], U_name=request.user.username)
                                new_mdord.save()
                                Cart.objects.filter(Username=request.user).get(
                                    p_id=mids[i]).delete()
                            new_ord = Orders(o_id=O_id, UserName=request.user.username, Date=date.today(),
                                             Time=datetime.now().strftime("%H:%M:%S"), Address=request.POST['Address'], Price=request.POST['Tprice'])
                            new_ord.save()
                            messages.success(
                                request, 'Order placed successfully.')
                            return redirect('/shopping')
                        except Exception as e:
                            print(type(e), e.args)
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
