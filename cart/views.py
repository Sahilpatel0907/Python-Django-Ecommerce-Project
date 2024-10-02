from django.shortcuts import render, get_object_or_404
from .cart import Cart
from shop.models import Product
from django.http import JsonResponse, HttpResponse
from django.contrib import messages


# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals})

def cart_add(request):
    cart = Cart(request)

    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')
        if product_id is None or product_qty is None:
            return JsonResponse({'error': 'Missing product ID or quantity'}, status=400)

        try:
            product_id = int(product_id)
            product_qty = int(product_qty)
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product, quantity=product_qty)
            cart_quantity = cart.__len__()
            messages.success(request, 'Product Added To Cart Successfully!')
            return JsonResponse({'qty': cart_quantity})

        except ValueError:
            return JsonResponse({'error': 'Invalid product quantity'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method or action'}, status=400)

def cart_update(request):  
   cart = Cart(request)  
   if request.method == 'POST' and request.POST.get('action') == 'post':  
      product_id = int(request.POST.get('product_id'))  
      product_qty = int(request.POST.get('product_qty'))  
  
      try:  
        cart.update(product=product_id, quantity=product_qty)  
        response = JsonResponse({'qty': product_qty})
        messages.success(request, ('Product Quantity Updated Successfully....'))
        return response  
      except Exception as e:  
        return JsonResponse({'error': str(e)}, status=400)

def cart_delete(request):  
    cart = Cart(request)  
    if request.method == 'POST' and request.POST.get('action') == 'post':  
        product_id = int(request.POST.get('product_id'))  
    
        try:  
            cart.delete(product=product_id)  
            response = JsonResponse({'message': 'Item deleted successfully'})
            messages.success(request, ('Product Removed From Cart Successfully....'))
            return response  
        except Exception as e:  
            return JsonResponse({'error': str(e)}, status=400)