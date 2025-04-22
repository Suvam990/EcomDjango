from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse


from django.views import View
from .models import Product,Category,Customer,Cart,OrderDetail,ProductImage




def home(request):
    products = None
    totalitem = 0
    
    if 'phone' in request.session:
        phone = request.session['phone']
        category = Category.get_all_categories()
        customer = Customer.objects.filter(phone=phone)
        totalitem = len(Cart.objects.filter(phone=phone))

        if customer.exists():
            name = customer[0].name

            category_id = request.GET.get('category')  # Fetch category from URL
            if category_id:
                products = Product.objects.filter(category_id=category_id)
            else:
                products = Product.objects.all()

            data = {
                'name': name,
                'product': products,
                'category': category,
                'totalitem': totalitem
            }
            return render(request, 'home.html', data)
        else:
            return redirect('login')
    else:
        return redirect('login')
    

    

def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    else:
        PostData = request.POST
        name = PostData.get('name')
        phone = PostData.get('phone')

        error_message = None

        value={
            'phone':phone,
            'name':name
        }

        customer = Customer(name=name,phone=phone)
        if not name:
            error_message ="Name is Required"
        elif not phone:
            error_message = "Phone is required" 
        elif len(phone)<10:
            error_message = "Mobile Number Must be 10 digite Long"

        elif customer.isExists():
            error_message = "Mobile Number is Alrady Exists"    

        if not error_message:
            messages.success(request, 'Congratulation !! Register Succesful')      

            customer.register()
            return redirect('signup',)
        else:
            data= {
                'error':error_message,
                'value':value
            }
            return render(request, "signup.html", data)
        

        # return HttpResponse("Signup Sucess")

    # return render(request, 'signup.html')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        phone = request.POST.get('phone')
        
        value = {
            'phone':phone
        }

        error_message=None
        customer= Customer.objects.filter(phone=request.POST['phone'])
        if customer:
            request.session['phone']=phone
            return redirect('home')
        else:
            error_message = "Mobile Number is invalied !!"
            data={
                'error':error_message,
                'value':value
            }

        return render (request, 'login.html', data) 



# class Login(view):
#     def get(self,request): 
#             return render(request, 'login.html')
  
#     def post(self,request):
def productdetail(request, pk):
    totalitem = 0
    product = get_object_or_404(Product, pk=pk)
    images = ProductImage.objects.filter(product=product)  # Get all images for this product

    item_alrady_in_cart = False
    if request.session.has_key('phone'):
        phone = request.session['phone']
        totalitem = Cart.objects.filter(phone=phone).count()
        item_alrady_in_cart = Cart.objects.filter(Q(product=product.id) & Q(phone=phone)).exists()
        customer = Customer.objects.filter(phone=phone)
        
        name = customer.first().name if customer.exists()else ""

    data = {
        'product': product,
        'images': images,  # Pass additional images
        'item_alrady_in_cart': item_alrady_in_cart,
        'name': name,
        'totalitem': totalitem
    }

    return render(request, 'productdetail.html', data)




def logout(request):
    if request.session.has_key('phone'):
        del request.session['phone']
        return redirect('login')   
    else:
        return redirect('login')
    

def add_to_cart(request):
    phone = request.session['phone']
    product_id = request.GET.get('prod_id')
    product_name = Product.objects.get(id=product_id)
    product = Product.objects.filter(id=product_id)
    
    for p in product:
        image = p.image
        price = p.price
        Cart(phone=phone,product=product_name,image=image,price=price).save()
        return redirect(f"/product-detail/{product_id}")


#===========show cart==========#
def show_cart(request):
    totalitem=0
    if request.session.has_key('phone'):
        phone = request.session['phone']
        totalitem - len(Cart.objects.filter(phone=phone))
        # cart = Cart.objects.filter(phone=phone)
        customer = Customer.objects.filter(phone=phone)
        for c in customer:
            name = c.name
            cart = Cart.objects.filter(phone=phone)
            total_price = sum(item.product.price * item.quantity for item in Cart.objects.filter(phone=phone))


            data={
                'name':name,
                'totalitem':totalitem,
                'cart':cart,
                'total_price':total_price
            }
            if cart:
                
                return render(request, 'show_cart.html', data)
            else:
                return render(request, 'empty_cart.html',data)
                
# def plus_cart(request):
#     if request.session.has_key('phone'):
#         phone = request.session['phone']
#         product_id = request.GET['prod_id']
#         cart = Cart.objects.get(Q(product=product_id) & Q(phone=phone))
#         cart.quantity+=1
#         cart.save()

#         data={
#             'quantity': cart.quantity

#         }
#         return JsonResponse(data)


def plus_cart(request):
    if request.session.has_key('phone'):
        phone = request.session['phone']
        product_id = request.GET.get('prod_id')

        try:
            cart = Cart.objects.get(Q(product=product_id) & Q(phone=phone))
            cart.quantity += 1
            cart.save()

            total_price = sum(item.product.price * item.quantity for item in Cart.objects.filter(phone=phone))

            data = {
                'quantity': cart.quantity,
                'total_price': total_price
            }
            return JsonResponse(data)

        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)

    return JsonResponse({'error': 'User not authenticated'}, status=401)

def minus_cart(request):
    if request.session.has_key('phone'):
        phone = request.session['phone']
        product_id = request.GET.get('prod_id')
        
        cart = get_object_or_404(Cart, Q(product=product_id) & Q(phone=phone))
        
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()  
        
        total_price = sum(item.product.price * item.quantity for item in Cart.objects.filter(phone=phone))

        data = {
            'quantity': cart.quantity if cart.id else 0,  
            'total_price': total_price
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'User not authenticated'}, status=401)

def remove_cart(request):
    if request.session.has_key('phone'):
        phone = request.session['phone']
        product_id = request.GET.get('prod_id')

        try:
            cart = Cart.objects.get(Q(product=product_id) & Q(phone=phone))
            cart.delete()

            total_price = sum(item.product.price * item.quantity for item in Cart.objects.filter(phone=phone))

            return JsonResponse({'total_price': total_price})

        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)

    return JsonResponse({'error': 'User not authenticated'}, status=401)



def remove_cart(request):
    if request.session.has_key('phone'):
        phone = request.session['phone']
        product_id = request.GET.get('prod_id')
        
        cart_item = get_object_or_404(Cart, Q(product=product_id) & Q(phone=phone))
        cart_item.delete()  

        total_price = sum(item.product.price * item.quantity for item in Cart.objects.filter(phone=phone))

        data = {
            'total_price': total_price
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'User not authenticated'}, status=401)



def checkout(request):
    totalitem=0

    if request.session.has_key('phone'):
        phone = request.session['phone']
        name = request.POST.get('name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        cart_product = Cart.objects.filter(phone=phone)
        for c in cart_product:
            quantity = c.quantity
            price = c.price
            product_name = c.product
            image = c.image

            OrderDetail(user = phone,product_name=product_name, image=image,quantity =quantity, price=price).save()
            cart_product.delete()

            totalitem - len(Cart.objects.filter(phone=phone))
        # cart = Cart.objects.filter(phone=phone)
            customer = Customer.objects.filter(phone=phone)
            for c in customer:
             name = c.name

             data = {
                'name':name,
                'totalitem':totalitem
                }
        # print(name,address,mobile)
            return render(request, 'empty_cart.html',data)
    else:
        return redirect('login')
    


def order(request):
    totalitem=0
    if request.session.has_key('phone'):
        phone = request.session['phone']    
        totalitem - len(Cart.objects.filter(phone=phone))
        # cart = Cart.objects.filter(phone=phone)
        customer = Customer.objects.filter(phone=phone)
        for c in customer:
             name = c.name
             order = OrderDetail.objects.filter(user=phone)

             data={
            'order':order,
            'name':name,
            'totalitem':totalitem
            }

             if order:
                return render(request, 'order.html',data)  
             else:
                 return render(request, 'emptyorder.html')
  
    else:
         return redirect('login')
    

def search(request):

    totalitem=0
    if request.session.has_key('phone'):
        phone = request.session['phone'] 
        query=request.GET.get('query')   
        # print('query')
        search = Product.objects.filter(name__contains=query)
        category = Category.get_all_categories()


        totalitem - len(Cart.objects.filter(phone=phone))
        # cart = Cart.objects.filter(phone=phone)
        customer = Customer.objects.filter(phone=phone)
        for c in customer:
             name = c.name

             data={
                 'name':name,
                 'totalitem':totalitem,
                 'search':search,
                 'category':category,
                 'query':query
             }

             return render(request, 'search.html',data)
    else:
        return redirect('login')
