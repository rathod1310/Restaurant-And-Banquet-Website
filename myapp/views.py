from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse
from django.contrib import messages
import requests
import random

###### This is common data to show cart box in all pages ######
def get_common_data(request):
	common_data = {}

	if 'email' in request.session:
		user = User.objects.get(email=request.session['email'])
		cart = Cart.objects.filter(user=user)
		common_data['cart'] = cart
		wishlist=Wishlist.objects.filter(user=user)
		request.session['wishlist_count']=len(wishlist)
		cart=Cart.objects.filter(user=user)
		request.session['cart_count']=len(cart)
		total_price = sum(i.quantity * i.food_item.price1 for i in cart)
		common_data['total_price'] = total_price

	return common_data

######################### LOGIN,REGISTER,LOGOUT #########################
def login (request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profile_pic']=user.profile_pic.url
				wishlist=Wishlist.objects.filter(user=user)
				request.session['wishlist_count']=len(wishlist)
				cart=Cart.objects.filter(user=user)
				request.session['cart_count']=len(cart)

				if user.user_type == "manager":
					return redirect('user')
				else:
					return redirect('index') 
			else:
				msg="Incorrect Password"
				return render(request,'login.html',{'msg':msg})
		except User.DoesNotExist:
			return render(request, 'register.html')
	else:
		return render(request,'login.html')

def register(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'register.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
						user_type=request.POST['user_type'],
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						address=request.POST['address'],
						city=request.POST['city'],
						state=request.POST['state'],
						pincode=request.POST['pincode'],
						password=request.POST['password'],
						profile_pic=request.FILES['profile_pic'],
					)
				msg="User Sign Up Successfully"
				return render(request,'login.html',{'msg':msg})
			else:
				msg="Password & Confirm Password Does Not Matched"
				return render(request,'register.html',{'msg':msg})
	else:
		return render(request,'register.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		return render(request,'login.html')
	except:
		return render(request,'login.html')

def change_password(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				msg="Password Changed Successfully"
				return render(request,'change_password.html',{'msg':msg})
			else:
				msg="New Password & Confirm New Password Does Not Matched"
				return render(request,'change_password.html',{'msg':msg})
		else:
			msg="Old Password Does Not Matched"
			return render(request,'change_password.html',{'msg':msg})
	else:
		context = get_common_data(request)
		return render(request,'change_password.html',context)

######################### HOME PAGE #########################
def index(request):
    context = get_common_data(request)
    try:
        user = User.objects.get(email=request.session.get('email'))
        if user.user_type == "customer":
            return render(request, "index.html", context)
        else:
            return redirect("user") 
    except User.DoesNotExist:
        return render(request, "index.html", context)

def track_order(request,pk):
	myorder=MyOrder.objects.filter(pk=pk)
	context = get_common_data(request)
	context.update({'myorder': myorder})
	return render(request, 'track_order.html',context)

######################### MENU PAGE #########################
def menu(request):
	categories = Category.objects.all() 
	food_item = Menu.objects.all()
	selected_category = request.GET.get('category')
	search_query = request.GET.get('search_query')

	common_data = get_common_data(request)
	cart = common_data.get('cart', [])
	total_price = common_data.get('total_price', 0)

	if selected_category:
		food_item = Menu.objects.filter(category_id=selected_category)
	elif search_query:
		food_item = Menu.objects.filter(name__icontains=search_query)

	sorting_option = request.GET.get('sorting', None)

	if sorting_option == "price_low_to_high":
		food_item = food_item.order_by('price1')
	elif sorting_option == "a_to_z":
		food_item = food_item.order_by('name')
	elif sorting_option == "z_to_a":
		food_item = food_item.order_by('-name')

	context = get_common_data(request)
	context.update({'categories':categories,'food_item':food_item,'selected_category':selected_category,"cart":cart,'total_price':total_price})
	return render(request, 'menu.html',context)


######################### CART,ADD-TO-CART,REMOVE-FROM-CART #########################
def cart(request):
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user)
	request.session['cart_count']=len(cart)
	for item in cart:
		item.total_price = item.food_item.price1 * item.quantity
	total_price = sum(item.quantity * item.food_item.price1 for item in Cart.objects.filter(user=user))
	context = get_common_data(request)
	context.update({"cart":cart,"total_price":total_price})
	return render(request,'cart.html',context)

def add_to_cart(request,pk):
	food_item=Menu.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	if not Cart.objects.filter(food_item=food_item, user=user).exists():
		Cart.objects.create(food_item=food_item, user=user)

		cart_count = Cart.objects.filter(user=user).count()
		request.session['cart_count'] = cart_count
	else:
		messages.info(request, f"{food_item.name} is already in your cart.")

	return redirect('menu')

def remove_from_cart(request,pk):
	food_item=Menu.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.get(user=user,food_item=food_item)
	cart.delete()
	return redirect('cart')

def increase_quantity(request,pk):
	food_item=Menu.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	cart = Cart.objects.get(user=user, food_item=food_item)
	cart.quantity += 1
	cart.save()
	return redirect('cart')

def decrease_quantity(request,pk):
	food_item=Menu.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	cart = get_object_or_404(Cart, user=user, food_item=food_item)
	if cart.quantity > 1:
		cart.quantity -= 1
		cart.save()
	else:
		cart.delete()
	return redirect('cart')

######################### WISHLIST,ADD-TO-WISHLIST,RREMOVE-FROM-WISHLIST #########################
def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlist)
	common_data = get_common_data(request)
	cart = common_data.get('cart', [])
	total_price = common_data.get('total_price', 0)
	context = get_common_data(request)
	context.update({'wishlist':wishlist,"cart":cart,'total_price':total_price})
	return render(request,'wishlist.html',context)

def add_to_wishlist(request,pk):
	food_item=Menu.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	if not Wishlist.objects.filter(food_item=food_item, user=user).exists():
		Wishlist.objects.create(food_item=food_item, user=user)

		wishlist_count = Wishlist.objects.filter(user=user).count()
		request.session['wishlist_count'] = wishlist_count
	else:
		messages.info(request, f":- {food_item.name} is already in your wishlist.")

	return redirect('menu')

def remove_from_wishlist(request,pk):
	food_item=Menu.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.get(user=user,food_item=food_item)
	wishlist.delete()
	return redirect('wishlist')

######################### GALLARY PAGE #########################
def gallary(request): 
	context = get_common_data(request)
	return render(request, 'gallary.html',context)

######################### CONTACT PAGE #########################
def contact(request): 
	context = get_common_data(request)
	return render(request, 'contact.html',context)

######################### LEAVE COMMENT(CONTACT PAGE) #########################
def leave_a_comment(request):
	if request.method == 'POST':
		Leave_A_Comment.objects.create(
				name=request.POST['name'],
				email=request.POST['email'],
				message=request.POST['message'],
			)
		messages.success(request, 'Your comment has been submitted successfully.')
		return redirect('contact') 
	
######################### TABLE BOOKING(RESERVATION) #########################
def reservation(request):
	user = None
	if 'email' in request.session:
		user = User.objects.get(email=request.session['email'])
	if request.method == 'POST':
		Reservation.objects.create(
				name=request.POST['name'],
				email=request.POST['email'],
				mobile=request.POST['mobile'],
				person=request.POST['person'],
				date=request.POST['date'],
				time=request.POST['time'],
				message=request.POST['message'],
			)
		return redirect('reservation')
	context = get_common_data(request)
	context.update({'user': user})
	return render(request, 'reservation.html',context)

######################### CHECKOUT PAGE #########################
def checkout(request):
    user = User.objects.get(email=request.session['email'])
    cart = Cart.objects.filter(user=user)
    total_price = sum(i.quantity * i.food_item.price1 for i in cart)

    if request.method == 'POST':
        payment_method = request.POST['payment_method']
        delivery_person_id = request.POST.get('delivery_person_id') 
        delivery_person = None
        
        if delivery_person_id:
            delivery_person = DeliveryPerson.objects.get(id=delivery_person_id)
        else:
            delivery_people = DeliveryPerson.objects.all()
            if delivery_people.exists():
                delivery_person = random.choice(delivery_people)

        MyOrder.objects.create(
            fname=request.POST['fname'],
            lname=request.POST['lname'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode'],
            food_item_name=request.POST.getlist('food_item_name()'),
            quantity=request.POST.getlist('quantity()'),
            price=request.POST.getlist('price()'),
            total_price=request.POST['total_price'],
            payment_method=payment_method,
            delivery_person=delivery_person
        )

        if payment_method == 'cash':
            return redirect('success')
        elif payment_method == 'stripe':
            return redirect('create_checkout_session')

    context = get_common_data(request)
    context.update({"user": user, "cart": cart, "total_price": total_price})
    return render(request, 'checkout.html', context)



######################### FAQ (HELP) PAGE #########################
def faq(request):
	context = get_common_data(request)
	return render(request, 'faq.html',context)

def profile(request): 
	user = User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.email=request.POST['email']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		user.city=request.POST['city']
		user.state=request.POST['state']
		user.pincode=request.POST['pincode']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		msg="Profile Update Successfully"
		request.session['profile_pic']=user.profile_pic.url
		return render(request,'profile.html',{'user':user,'msg':msg,'cart':cart})
	else:
			context = get_common_data(request)
			context.update({'user':user,'cart':cart})
			return render(request,'profile.html',context)

######################### NYBOOKINGS (RESERVATION HISTORY) PAGE #########################
def mybookings(request):
	user=User.objects.get(email=request.session['email'])
	reservation=Reservation.objects.filter(name=user)
	context = get_common_data(request)
	context.update({"reservation":reservation})
	return render(request, 'mybookings.html',context)

######################### NYBOOKINGS (RESERVATION HISTORY) PAGE #########################
def myorders(request):
	user=User.objects.get(email=request.session['email'])
	myorder=MyOrder.objects.filter(fname=user)
	context = get_common_data(request)
	context.update({'myorder':myorder})
	return render(request, 'myorders.html',context)

######################### FEEDBACK PAGE #########################
def feedback(request):
	if request.method == 'POST':
		Feedback.objects.create(
				name=request.POST['name'],
				email=request.POST['email'],
				rating=request.POST['rating'],
				message=request.POST['message'],
			)
		return redirect('feedback')
	context = get_common_data(request) 
	return render(request, 'feedback.html',context)

######################### FEEDBACK PAGE #########################
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
	user=User.objects.get(email=request.session['email'])
	cart = Cart.objects.filter(user=user)
	total_price = sum(i.quantity * i.food_item.price1 for i in cart)
    
	session = stripe.checkout.Session.create(
	    payment_method_types=['card'],
	    line_items=[
	        {
	            'price_data': {
	                'currency': 'INR',
	                'product_data': {
	                    'name': 'Your Product Name',
	                },
	                'unit_amount': int(total_price * 100),  # Amount in cents
	            },
	            'quantity': 1,
	        },
	    ],
	    mode='payment',
	    success_url=request.build_absolute_uri(reverse('success')),
	    cancel_url=request.build_absolute_uri(reverse('cancel')),
	)
	return redirect(session.url)

def success(request):
	context = get_common_data(request)
	clear_cart(request)
	return render(request, 'success.html',context)

def cancel(request):
    return render(request, 'cancel.html')

def clear_cart(request):
	user=User.objects.get(email=request.session['email'])
	Cart.objects.filter(user=user).delete()

def cancel_reservation(request, pk):
    try:
        user = User.objects.get(email=request.session.get('email'))
        reservation = Reservation.objects.get(pk=pk)
        reservation_datetime = timezone.make_aware(datetime.combine(reservation.date, reservation.time))
        time_difference = reservation_datetime - timezone.now()
        if reservation.date == timezone.now().date() and time_difference.total_seconds() > 7200:
            msg = "Sorry, you cannot cancel this reservation as it is less than 2 hours away from now."
        else:
            reservation.delete()
            msg = "Reservation canceled successfully."
    except User.DoesNotExist:
        msg = "User does not exist."
    except Reservation.DoesNotExist:
        msg = "Reservation does not exist."
    return HttpResponse('<script>alert("' + msg + '"); window.history.back();</script>')



def allocate_delivery_person(request,pk):
	delivery_people = DeliveryPerson.objects.all()
	user = User.objects.get(email=request.session.get('email'))
	myorder = MyOrder.objects.get(pk=pk)
	if delivery_people.exists():
		delivery_person = random.choice(delivery_people)
		myorder.delivery_person = delivery_person
		myorder.status = 'IN_PROGRESS'
		myorder.save()
		return True
	else:
		return False


def cancle_order(request, pk):
	try:
		user = User.objects.get(email=request.session.get('email'))
		myorder = MyOrder.objects.get(pk=pk)
		
		if myorder.status == 'PENDING':
			myorder.status = 'CANCELLED'
			myorder.save()
			msg = "Order Cancelled Successfully."
		else:
			msg = "Sorry, you cannot cancel this Order beacause the order is prepared now."
	except User.DoesNotExist:
		msg = "User does not exist."
	except MyOrder.DoesNotExist:
		msg = "Myorder does not exist."

	# Return a script to display the message in a popup and navigate back to the previous page
	return HttpResponse('<script>alert("' + msg + '"); window.history.back();</script>')

def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(mobile=request.POST['mobile'])
			otp=random.randint(1000,9999)
			mobile=user.mobile
			url = "https://www.fast2sms.com/dev/bulkV2"
			querystring = {"authorization":"DwF5Auzh16qo3fXC2JMSTcOiyBEZmWH0eR8GIg4NbQrpUnKsjvhz0YwyOCGvHJEFuXRrTc7feDVaM1NA","variables_values":str(otp),"route":"otp","numbers":str(mobile)}
			headers = {'cache-control': "no-cache"}
			response = requests.request("GET", url, headers=headers, params=querystring)
			print(response.text)
			msg="OTP Sent To Your Registerd Mobile Number"
			return render(request,'forget_password/otp.html',{'mobile':mobile,'otp':otp,'msg':msg})
		except:
			msg="Mobile Number Not Registered"
			return render(request,'forget_password/forgot_password.html',{'msg':msg})
	else:
		context = get_common_data(request)
		return render(request,'forget_password/forgot_password.html',context)

def verify_otp(request):
	mobile=request.POST['mobile']
	otp=request.POST['otp']
	uotp=request.POST['uotp']

	if otp==uotp:
		return render(request,'forget_password/new_password.html',{'mobile':mobile})
	else:
		msg="Invalid OTP"
		return render(request,'forget_password/otp.html',{'mobile':mobile,'otp':otp,'msg':msg})

def new_password(request):
	mobile=request.POST['mobile']
	np=request.POST['new_password']
	cnp=request.POST['cnew_password']

	if np==cnp:
		user=User.objects.get(mobile=mobile)
		user.password=np
		user.save()
		msg="Password Changed Succesfully"
		return render(request,'forget_password/forgot_password.html',{'msg':msg})
	else:
		msg="New Password & Confirm New Password Does Not Matched"
		return render(request,'forget_password/new_password.html',{'mobile':mobile,'msg':msg})
	
######################### MANAGER #########################
def user(request):
	user = User.objects.all() 
	return render(request, 'manager/user.html',{'user':user})

def show_user_details(request,pk):
    user = User.objects.get(pk=pk)
    return render(request, 'manager/show_user_details.html', {'user': user})

def delivery_persons(request):
	delivery_persons = DeliveryPerson.objects.all() 
	return render(request, 'manager/delivery_persons.html',{'delivery_persons':delivery_persons})

def feedbacks(request):
	feedbacks = Feedback.objects.all()
	return render(request, 'manager/feedbacks.html',{'feedbacks':feedbacks})

def category(request):
	category = Category.objects.all()
	if request.method == 'POST':
		Category.objects.create(
				name=request.POST['name'],
			)
		return redirect('category')
	return render(request, 'manager/category.html',{'category':category})

def delete_category(request,pk):
	category= Category.objects.filter(pk=pk)
	category.delete()
	return redirect('category')
		

def food_items(request):
	food_items = Menu.objects.all()
	category = Category.objects.all()
	return render(request, 'manager/food_items.html',{'food_items':food_items,'category':category})

def delete_food_items(request,pk):
	food_items= Menu.objects.filter(pk=pk)
	food_items.delete()
	return redirect('food_items')

def add_food_item(request):
	category = Category.objects.all() 
	if request.method == 'POST':
		category = request.POST['category']
		category = Category.objects.get(name=category)
		Menu.objects.create(
				category=category,
				name=request.POST['name'],
				description=request.POST['description'],
				price1=request.POST['price1'],
				price2=request.POST['price2'],
				image=request.FILES['image'],
					)
		return redirect('food_items')
	return render(request, 'manager/add_food_item.html',{'category':category})

def add_delivery_person(request):
	if request.method == 'POST':
		DeliveryPerson.objects.create(
				name=request.POST['name'],
				vehicle_number=request.POST['vehicle_number'],
				profile_pic=request.FILES['profile_pic'],
			)
		return redirect('delivery_persons')
	return render(request, 'manager/add_delivery_person.html')

def delete_delivery_person(request,pk):
	delivery_persons = DeliveryPerson.objects.filter(pk=pk)
	delivery_persons.delete()
	return redirect('delivery_persons')

def orders(request):
	myorders = MyOrder.objects.all() 
	return render(request, 'manager/orders.html',{'myorders':myorders})

def show_order_details(request,pk):
    myorder = MyOrder.objects.get(pk=pk)
    return render(request, 'manager/show_order_details.html', {'myorder': myorder})

def reservations(request):
	reservations = Reservation.objects.all() 
	return render(request, 'manager/reservations.html',{'reservations':reservations})

def edit_food_item(request,pk): 
	food_items= Menu.objects.get(pk=pk)
	category = Category.objects.all()
	current_category = food_items.category.name if food_items.category else None
	if request.method=="POST":
		food_items.name=request.POST['name']
		food_items.description=request.POST['description']
		food_items.price1=request.POST['price1']
		food_items.price2=request.POST['price2']
		category_name = request.POST.get('category')
		food_items.category = Category.objects.get(name=category_name)
		try:
			food_items.image=request.FILES['image']
		except:
			pass
		food_items.save()
		msg="Food Item Update Successfully"
		request.session['image']=food_items.image.url
		current_category = food_items.category.name if food_items.category else None
		return render(request,'manager/edit_food_item.html',{'food_items':food_items,'msg':msg,'current_category':current_category,'category':category})
	else:
			context = get_common_data(request)
			context.update({'food_items':food_items})
	return render(request,'manager/edit_food_item.html',{'food_items':food_items,'category':category,'current_category':current_category})