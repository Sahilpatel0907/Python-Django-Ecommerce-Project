from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingAddressForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from shop.models import Product, CustomerProfile
import datetime


# Create your views here.

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        order_items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            if status == "true":
                order = Order.objects.filter(id = pk)
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped = now)
                messages.success(request, "Order marked as shipped.")
            else:
                order = Order.objects.filter(id = pk)
                order.update(shipped=False)
                messages.success(request, "Order marked as not shipped.")


        return render(request, 'payment/orders.html', {'order': order, 'order_items': order_items})


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped = now)
            messages.success(request, "Order marked as shipped.")
        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})
    else:
        messages.error(request, "Only superusers can access this page.")
        return redirect('home')



def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            now = datetime.datetime.now()
            order.update(shipped=False)
            messages.success(request, "Order marked as shipped.")
        return render(request, 'payment/shipped_dash.html', {'orders':orders})
    else:
        messages.error(request, "Only superusers can access this page.")
        return redirect('home')



def process_order(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to place an order.")
        return redirect('login')  # Redirect to the login page

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        my_shipping = request.session.get('my_shipping')

        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # Ensure shipping information exists
        if my_shipping:
            full_name = my_shipping.get('shipping_full_name', '')
            email = my_shipping.get('shipping_email', '')
            shipping_address = (
                f"{my_shipping.get('shipping_address1', '')}\n"
                f"{my_shipping.get('shipping_address2', '')}\n"
                f"{my_shipping.get('shipping_city', '')}\n"
                f"{my_shipping.get('shipping_state', '')}\n"
                f"{my_shipping.get('shipping_zipcode', '')}\n"
                f"{my_shipping.get('shipping_country', '')}"
            )
            amount_pay = totals

            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_pay=amount_pay)
            create_order.save()

            order_id = create_order.pk
            for product in cart_products:
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                
                for key, value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=int(value), price=price)
                        create_order_item.save()

            # Delete Our Cart

            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]

            # Delete Cart From Database
            current_user = CustomerProfile.objects.filter(user__id = request.user.id)
            current_user.update(old_cart='')


            if payment_form.is_valid():
                # Process the payment here (e.g., handle payment)
                
                messages.success(request, "Your order has been placed successfully.")
                return redirect('home')
            else:
                messages.error(request, "Please correct the payment information.")
        else:
            messages.error(request, "Shipping information is missing.")
    else:
        messages.error(request, "Access denied.")

    return redirect('home')



def billing_info(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    shipping_info = None
    billing_form = PaymentForm()

    if request.user.is_authenticated:
        shipping_info = ShippingAddress.objects.get(user=request.user)

        request.session['my_shipping'] = {
            'shipping_full_name': shipping_info.shipping_full_name,
            'shipping_email': shipping_info.shipping_email,
            'shipping_address1': shipping_info.shipping_address1,
            'shipping_address2': shipping_info.shipping_address2,
            'shipping_city': shipping_info.shipping_city,
            'shipping_state': shipping_info.shipping_state,
            'shipping_zipcode': shipping_info.shipping_zipcode,
            'shipping_country': shipping_info.shipping_country,
        }

        if request.method == 'POST':
            return render(request, 'payment/billing_info.html', {
                'cart_products': cart_products,
                'quantities': quantities,
                'totals': totals,
                'shipping_info': shipping_info,
                'billing_form': billing_form, 
            })
        
    else:
        billing_form = PaymentForm()
        return render(request, 'payment/billing_info.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_info': shipping_info, 'billing_form':billing_form})

    return render(request, 'payment/billing_info.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_info': shipping_info, 'billing_form':billing_form})


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form})
    else:
        shipping_form = ShippingAddressForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals})

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})