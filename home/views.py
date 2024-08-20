import numpy as np
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from PIL import Image
from django.views.decorators.cache import cache_control #new
from django.core.paginator import Paginator
from .models import *
from .forms import *
import cv2
import json


import os

import cvzone
from cvzone.PoseModule import PoseDetector

global select_shirt
# Create your views here.
def home(request):
    return render(request, 'home.html')

def product(request):
    return render(request, 'product.html')

@cache_control(no_chache=True,must_revalidate=True,no_store=True)
def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            
            firstname = firstname.strip()
            lastname = lastname.strip()
            email = email.strip()
            username = username.strip()
            password1 = password1.strip()
            password2 = password2.strip()

            if password1==password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already taken')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    print("Email already registered")
                    messages.info(request, 'Email taken')
                    return redirect('register')
                else:
                    user = User.objects.create_user(email=email, password=password1, username=username, first_name=firstname, last_name=lastname)
                    user.save();
                    print('user created')
                    messages.info(request, 'user created')
                    return render(request, 'login.html')
        else:
            return render(request, 'register.html')
    else:
        messages.info(request, 'To Create new account please logout first')
        return redirect('home')

    
    
@cache_control(no_chache=True,must_revalidate=True,no_store=True)
def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            username = username.strip()
            password = password.strip()
            user = auth.authenticate(username=username,password=password)
            

            if user is not None :
                print("you are login")
                messages.info(request, "Wellcome "+username)
                auth.login(request, user)
                request.session['username'] = username
                s_user= request.session['username']

                print('you are ' , request.session.get('username'))
                print('user = ', s_user)
                return redirect("home")
            else:
                messages.info(request, "invalid username or password")
                return redirect("login")

        else:
            return render(request,'login.html')
    else:
        messages.info(request, "your account is already login! please logout first")
        return redirect('home')
    
@cache_control(no_chache=True,must_revalidate=True,no_store=True)
def logout(request):
    auth.logout(request)
    request.session.flush()
    request.session.clear_expired()
    print('you are ' , request.session.get('username'))
    return redirect('home')

@cache_control(no_chache=True,must_revalidate=True,no_store=True)
def manage_products(request):
    if request.user.is_staff:
        adds = products.objects.all()
        paginator = Paginator(adds, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        nums = 'a' * page_obj.paginator.num_pages
        return render(request, 'manage_products.html', {'page_obj': page_obj,'nums': nums})
    else:
        return HttpResponse('you are not staff')

@cache_control(no_chache=True,must_revalidate=True,no_store=True)
def disable(request, id):
    add = products.objects.get(id=id)
    form = disable_productForm(request.POST, request.FILES, instance=add)
    form.save()
    return redirect('manage_products')

@cache_control(no_chache=True,must_revalidate=True,no_store=True)
def add_product(request):
    if request.method == 'POST':
        form = productForm(request.POST, request.FILES)
        form.save()

        return redirect('manage_products')
    else:
        return render(request, 'add_product.html')

@cache_control(no_chache=True,must_revalidate=True,no_store=True)    
def edit(request, id):
    if request.method == 'POST':
        add = products.objects.get(id=id)
        form = productForm(request.POST, request.FILES, instance=add)
        form.save()
        return redirect('manage_products')
    else:
        add = products.objects.get(id=id)
        return render(request, 'edit.html', {'add' : add})

@cache_control(no_chache=True,must_revalidate=True,no_store=True)
def delete_product(request, id):
    print(id)
    add = products.objects.get(id=id)
    add.delete()
    return redirect('manage_products')

@cache_control(no_chache=True,must_revalidate=True,no_store=True)
def view_product(request, id):
    add = products.objects.get(id=id)
    dests = []
    i=0
    dests_new = products.objects.filter(disable=False).order_by('?')
    # dests = dests[10]
    for val in dests_new:
        if i<4:
            print(i)
            dests.append(val)
            i = i+1
        else:
            break

    return render(request, 'product.html',{'add':add,'dests':dests})

@cache_control(no_chache=True,must_revalidate=True,no_store=True)
def shop(request):
    adds = products.objects.filter(disable=False).order_by('-id')
    paginator = Paginator(adds, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    nums = 'a' * page_obj.paginator.num_pages
    return render(request, 'shop.html',{'page_obj': page_obj,'nums': nums})

@cache_control(no_chache=True,must_revalidate=True,no_store=True)
def manage_staff(request):
    if request.user.is_superuser:
        users = User.objects.filter(is_staff=True)
        paginator = Paginator(users, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        nums = 'a' * page_obj.paginator.num_pages
        return render(request,'manage_staff.html', {'page_obj': page_obj,'nums': nums})

    else:
        return HttpResponse('you are not admin')
    
@cache_control(no_chache=True,must_revalidate=True,no_store=True)
def manage_users(request):
    if request.user.is_superuser:
        users = User.objects.filter(is_staff=False)
        paginator = Paginator(users, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        nums = 'a' * page_obj.paginator.num_pages
        return render(request,'manage_users.html', {'page_obj': page_obj,'nums': nums})
    else:
        return HttpResponse('you are not admin')


@cache_control(no_chache=True,must_revalidate=True,no_store=True)
def add_staff(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                username = request.POST['username']
                email = request.POST['email']
                password1 = request.POST['password1']
                password2 = request.POST['password2']
                is_staff = request.POST['is_staff']
                
                print(is_staff)

                firstname = firstname.strip()
                lastname = lastname.strip()
                email = email.strip()
                username = username.strip()
                password1 = password1.strip()
                password2 = password2.strip()

                if password1==password2:
                    if User.objects.filter(username=username).exists():
                        messages.error(request, 'Username already taken')
                        return redirect('add_staff')
                    elif User.objects.filter(email=email).exists():
                        print("Email already registered")
                        messages.info(request, 'Email taken')
                        return redirect('add_staff')
                    else:
                        user = User.objects.create_user(email=email, password=password1, username=username, first_name=firstname, last_name=lastname, is_staff=is_staff )
                        user.save();
                        print('user created')
                        messages.info(request, 'user created')
                        return redirect('manage_staff')
            else:
                return render(request,'add_staff.html')
        else:
            return HttpResponse('you are not admin')
    else:
        messages.info(request, 'Please login First')
        return redirect('login')

@cache_control(no_chache=True,must_revalidate=True,no_store=True)    
def delete_user(request, id,username):
    if request.user.is_authenticated:
        print(id)
        print(username)
        user = User.objects.get(id=id,username=username)
        if user.is_staff==True and user.is_superuser==True:
            messages.info(request, "You can not delete Superuser")
            return redirect('manage_staff')
        elif user.is_staff==True and user.is_superuser==False:
            user.delete()
            messages.info(request, "Staff delete Successfully")
            return redirect('manage_staff')
        else:
            user.delete()
            messages.info(request, "User delete Successfully")
            return redirect('manage_users')
    else:
        messages.info(request, "Please login First")
        return redirect('login')


@cache_control(no_chache=True,must_revalidate=True,no_store=True)
def contact(request):
    if request.method == 'POST':
        form = contactForm(request.POST)
        form.save()
        messages.info(request, "Your message is send to Admin")
        return redirect('contact')
    else:
        return render(request, 'contactus.html')



def try_now(request,id):
    obj = products.objects.get(id=id)
    print(obj.name)
    print(obj.img)
    path22=obj.img.url
    print(path22)
    path = "media"+path22
    print(path)
    body(path)


    obj = products.objects.get(id=id)

    global select_shirt
    select_shirt = obj.id
    print(select_shirt)
    # selected_shirt_path = ""
    try_button = None
    if 'shirt' in obj.name:
        try_button= True
    else:
        try_button= False
        

    return redirect("/view_product/{}".format(select_shirt))


def body(path):
    # video_path = os.path.join(os.getcwd(), "test_videos","sample1.mp4")
    cap = cv2.VideoCapture(0)
    detector = PoseDetector()
    scaling_pixel = 25
    print(path)
    shirt = path
    # print(listShirts)
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL) 
    while True:
        success, img = cap.read()
        # img = cv2.flip(img, 1)
        img = detector.findPose(img, draw=False) # points detection
        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
        try:
            if lmList:
                left_shoulder = lmList[11]
                right_shoulder = lmList[12]
                left_hip = lmList[23]
                right_hip = lmList[24]

                # imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[0]), cv2.IMREAD_UNCHANGED)
                imgShirt = cv2.imread(shirt, cv2.IMREAD_UNCHANGED)

                print("i ma here")
                widthOfShirt = abs(int((left_shoulder[0] - right_shoulder[0])))
                height_of_shirt = abs(int((right_hip[1] - right_shoulder[1])))

                width_currentScale = abs((left_shoulder[0] - right_shoulder[0]) / img.shape[1])
                height_currentScale = abs((right_hip[1] - right_shoulder[1]) / img.shape[0])
                offset = (int(60 * width_currentScale), int(66 * height_currentScale))

                widthOfShirt += offset[0]
                height_of_shirt += offset[1]

                print(widthOfShirt)

                imgShirt = cv2.resize(imgShirt, (widthOfShirt, height_of_shirt))


                try:
                    x1, y1 = right_shoulder[0], right_shoulder[1]
                    pos = (x1 - offset[0], y1 - offset[1])
                    img = Image.fromarray(img)
                    imgShirt = Image.fromarray(imgShirt)
                    img.paste(imgShirt, pos, mask=imgShirt)
                    img = np.asarray(img)
                except Exception as e:
                    print(f"system fail: Error {str(e)}")
                    pass
        except Exception as e:
            print(f"system2 fail, Error: {str(e)}")
            pass
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    cap.release()                           # Destroys the cap object
    cv2.destroyAllWindows() 

# def buy_now(request, id,username,name,price):
def buy_now(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            id = request.POST['id']
            
            username = request.POST['username']
            name = request.POST['name']
            price = request.POST['price']
            print(type(price))
            price = int(price)
            quantity = request.POST['quantity']
            quantity = int(quantity)
            TotalPrice = price * quantity

            TotalPrice = int(TotalPrice)
            print(TotalPrice)
            info = Buyer_info.objects.create(Buyer_name=username, product_id=id, Product_name=name, quantity=quantity, total_price=TotalPrice)
            info.save();
        messages.info(request, 'your order is send to the seller it will take 3 to 5 working days to deliver to you')
        return redirect('shop')
    else:
        messages.info(request, 'Please login first')
        return redirect('login')

def contactUS(request):
    if request.user.is_authenticated:
        con = contact_message.objects.all()
        paginator = Paginator(con, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        nums = 'a' * page_obj.paginator.num_pages
        # return render(request,'manage_staff.html', {'page_obj': page_obj,'nums': nums})
        return render(request, 'contact.html', {'page_obj': page_obj,'nums': nums})
    else:
        messages.info(request, 'Please login first')
        return redirect('login')
    
def delete_mess(request, id):
    mess = contact_message.objects.get(id=id)
    mess.delete()
    messages.info(request, 'message delete sucessfully')
    return redirect('contactUS')

def orders(request):
    if request.user.is_authenticated:
        con = Buyer_info.objects.all()
        paginator = Paginator(con, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        nums = 'a' * page_obj.paginator.num_pages
        # return render(request,'manage_staff.html', {'page_obj': page_obj,'nums': nums})
        return render(request, 'orders.html', {'page_obj': page_obj,'nums': nums})
    else:
        messages.info(request, 'Please login first')
        return redirect('login')