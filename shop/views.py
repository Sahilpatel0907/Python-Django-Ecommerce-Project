from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import Product, Category, CustomerProfile

from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from.forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
import json


# Create your views here.

def search_view(request):
    query = request.GET.get('query', '').strip()
    products = Product.objects.all()

    if query:
        search_terms = query.split()
        for term in search_terms:
            products = products.filter(name__icontains=term) | products.filter(description__icontains=term) | products.filter(category__name__icontains=term)

    products = products.distinct()

    return render(request, 'search.html', {'products': products, 'query': query})

def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = CustomerProfile.objects.get(user__id=request.user.id)
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)
        
		if form.is_valid() or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
    #  , 'shipping_form':shipping_form
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')



def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password updated successfully.....')
                return redirect('update_user')
            else:
                for error in (form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.error(request, 'You Must be logged in')

@login_required 
def update_user(request):
    current_user = request.user
    user_form = UpdateUserForm(request.POST or None, instance=current_user)

    if request.method == 'POST':
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'User Profile updated successfully.')
            return redirect('home')
    
    return render(request, 'update_user.html', {'user_form': user_form})
   
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})

def category(request, foo):
    foo = foo.replace('-', '')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.success(request, ('This Category Does Not Exist'))
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Do some shopping cart stuff
            current_user = CustomerProfile.objects.get(user__id=request.user.id)
            # Get their saved cart from database
            saved_cart = current_user.old_cart
            # Convert database string to python dictionary
            if saved_cart:
                # Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dictionary to our session
                # Get the cart
                cart = Cart(request)
                # Loop thru the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
                
            messages.success(request, 'Logged in successfully.')
            return redirect('home')
        else:
            messages.success(request, 'There was an error, please try again!')
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You Have Been Logged out successfully.')
    return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
			return redirect('update_info')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})