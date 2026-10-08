from itertools import product

from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from shop.models import Product
from cart.models import Cart,Order
from cart.forms import Order_Form
from cart.models import Order_items
from shop.models import CustomUser
from decimal import Decimal
import razorpay
import os
from django.contrib import messages


# Create your views here.

class AddtoCart(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        try:
            c=Cart.objects.get(user=u,product=p)
            c.quantity+=1  #increments the quantity value by 1
            c.save()
        except: #if product not inside cart table creates a new cart record
            c=Cart.objects.create(user=u,product=p,quantity=1)
            c.save()
        return redirect('cart:cartview')


class CartView(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.quantity*i.product.price
        return render(request,'cart.html',{'cart':c,'total':total})




class CartDecrement(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        try:
            c=Cart.objects.get(user=u,product=p)
            if c.quantity>1:   # if cart object quantity is greater than 1
                c.quantity-=1  #decrements quantity by 1
                c.save()
            else:
                c.delete()    # if cart object quantity is 1 then deletes the cart object

        except:
            pass
        return redirect('cart:cartview')



class CartRemove(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        try:
            c=Cart.objects.get(user=u,product=p)
            c.delete()
        except:
            pass
        return redirect('cartview')



def check_stock(c):
    stock=True
    for i in c:
        if i.product.stock<i.quantity:
            stock=False
            break
    return stock


class OrderForm(View):
    def post(self, request):
        u = request.user
        response_payment = None
        form_instance = Order_Form(request.POST)

        if form_instance.is_valid():
            order_object = form_instance.save(commit=False)
            order_object.user = u
            order_object.save()

            c = Cart.objects.filter(user=u) #cart items selected by particular user
            stock=check_stock(c)
            if stock:
                # create order items
                for i in c:
                    Order_items.objects.create(
                        order=order_object,
                        product=i.product,
                        quantity=i.quantity
                    )

                total = Decimal('0.00')
                for i in c:
                    total += i.quantity * i.product.price
                total_paise = int(total * 100)



                if order_object.payment_method=="ONLINE":
                # Razorpay
                    client = razorpay.Client(
                        auth=(os.getenv('RAZORPAY_KEY_ID'), os.getenv('RAZORPAY_KEY_SECRET'))
                    )
                    response_payment = client.order.create({"amount":total_paise,"currency":"INR","payment_capture": 1})

                    order_id=response_payment['id']
                    order_object.order_id=order_id
                    order_object.is_ordered=True
                    order_object.amount=total
                    order_object.save()
                    return render(request, 'payment.html', {'payment': response_payment, 'name': u.username,'method': 'ONLINE' })

                elif order_object.payment_method=="COD":
                    order_object.is_ordered=True
                    order_object.amount = total
                    order_object.save()
                    items = Order_items.objects.filter(order=order_object)
                    for i in items:
                        i.product.stock -= i.quantity  # decrements each item stock
                        i.product.save()

                    # To delete cart of the current user

                    c = Cart.objects.filter(user=u)
                    c.delete()
                else:
                    pass

                return render(request, 'payment_success.html',{'method': 'COD'} )
            else:
                messages.error(request,"Currently items not available")
                return render(request,'payment.html',)
    def get(self,request):
        form_instance=Order_Form()
        return render(request,'orderform.html',{'form':form_instance})



from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt,name='dispatch') #to avoid csrf protection error
class Paymentsuccess(View):
    def post(self,request,i):
        user=CustomUser.objects.get(username=i)
        login(request, user) #To add the current user into session again
        response=request.POST
        print(response)    #payment confirmation send  by razorpay to our application


        #To change ordered field to True after completion of payment
        o=Order.objects.get(order_id=response['razorpay_order_id'])
        o.is_ordered=True
        o.save()


        #To change the product stock first filter ordered items
        items=Order_items.objects.filter(order=o)
        for i in items:
            i.product.stock-=i.quantity   #decrements each item stock
            i.product.save()

        #To delete cart of the current user

        c=Cart.objects.filter(user=user)
        c.delete()
        return render(request,'payment_success.html')




class OrderSummary(View):
    def get(self,request):
        o=Order.objects.filter(user=request.user,is_ordered=True)
        return render(request,'ordersummary.html',{'items':o})



