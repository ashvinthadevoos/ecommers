from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from customer.forms import RegistrationForm,LoginForm,ReviewForm
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from store.models import Products,Carts,Orders,Offers,Reviews
from django.utils.decorators import method_decorator
# Create your views here.


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)
    return wrapper

def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect('signin')

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,'signup.html',{'form':form})

    def post(self,request,*args,**kwrags):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'account created succesfully')
            return redirect('signup')
        else:
            messages.error(request,'account creation failed')
            return render(request,'signup.html',{'form':form})

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,'signin.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect('index')
            else:
                return render(request,'signin.html',{'form':form})

@method_decorator(signin_required,name='dispatch')
class IndexView(View):
    def get(self,request,*args,**kwargs):
        qs=Products.objects.all()
        return render(request,'index.html',{'products':qs})

@method_decorator(signin_required,name='dispatch')
class ProductDetailView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Products.objects.get(id=id)
        return render(request,'product-detail.html',{'product':qs})

@method_decorator(signin_required,name='dispatch')
class AddToCartView(View):


    def post(self,request,*args,**kwargs):
        qty=request.POST.get('qty')
        user=request.user
        id=kwargs.get('id')
        product=Products.objects.get(id=id)
        cart=Carts.objects.create(qty=qty,product=product,user=user)
        return redirect('index')

@method_decorator(signin_required,name='dispatch')
class MyCartView(View):

    def get(self,request,*args,**kwargs):
        qs=Carts.objects.filter(user=request.user,status='in-cart')
        return render(request,'cart-list.html',{'carts':qs})

@method_decorator(signin_required,name='dispatch')
class CartRemoveView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        obj=Carts.objects.get(id=id)
        obj.status="cancelled"
        obj.save()
        return redirect('cart-list')

@method_decorator(signin_required,name='dispatch')
class MakeOrderView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        qs=Carts.objects.get(id=id)
        return render(request,'checkout.html',{'cart':qs})

    def post(self,request,*args,**kwargs):
        user=request.user
        adress=request.POST.get('adress')
        id=kwargs.get('id')
        cart=Carts.objects.get(id=id)
        product=cart.product
        Orders.objects.create(product=product,user=user,address=adress)
        cart.status='order-placed'
        cart.save()
        return redirect('index')

@method_decorator(signin_required,name='dispatch')
class MyOrdersView(View):
     def get(self,request,*args,**kwargs):
        qs=Orders.objects.filter(user=request.user,).exclude(status='cancelled')
        return render(request,'order-list.html',{'order':qs})

@method_decorator(signin_required,name='dispatch')
class OrderCancelView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        Orders.objects.filter(id=id).update(status='cancelled')
        return redirect('orders')

@method_decorator(signin_required,name='dispatch')
class DiscountProductView(View):

    def get(self,request,*args,**kwargs):
        qs=Offers.objects.all()
        return render(request,'offer-products.html',{'offers':qs})

@method_decorator(signin_required,name='dispatch')
class ReviewAddView(View):

    def get(self,request,*args,**kwargs):
        form=ReviewForm()
        return render(request,'review-add.html',{'form':form})

    def post(self,request,*args,**kwargs):
        form=ReviewForm(request.POST)
        id=kwargs.get('id')
        pro=Products.objects.get(id=id)
        if form.is_valid():
            form.instance.user=request.user
            form.instance.product=pro
            form.save()
            return redirect('index')
        else:
            return render(request,'review-add.html',{'form':form})