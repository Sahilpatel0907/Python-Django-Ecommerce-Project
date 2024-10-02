from shop.models import Product, CustomerProfile
from decimal import Decimal
import json

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
		# Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = CustomerProfile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = CustomerProfile.objects.filter(user = self.request.user)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart=str(carty))
    
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):  
        product_id = str(product)  
        product_qty = str(quantity)  
            
        mycart = self.cart  
        mycart[product_id] = product_qty  
        self.session.modified = True
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = CustomerProfile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
        return mycart

    def delete(self, product):  
        product_id = str(product)  
        mycart = self.cart  
        if product_id in mycart:  
            del mycart[product_id]  
            self.session.modified = True  
            if self.request.user.is_authenticated:
            # Get the current user profile
                current_user = CustomerProfile.objects.filter(user__id=self.request.user.id)
                # Convert {'3':1, '2':4} to {"3":1, "2":4}
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
                # Save carty to the Profile Model
                current_user.update(old_cart=str(carty))
        return mycart
    
    def cart_total(self):  
        product_ids = self.cart.keys()  
        products = Product.objects.filter(id__in=product_ids)  
        quantities = self.cart  
        total = Decimal(0) 
        for key, value in quantities.items():  
            key = int(key)
            product = next((p for p in products if p.id == key), None)
            if product is not None:
                price = product.sale_price if product.is_sale else product.price
                if isinstance(price, str):  
                    price = Decimal(price)
                total += price * Decimal(value) 
            else:
                continue
        return total