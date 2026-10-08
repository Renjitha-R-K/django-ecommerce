from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse_lazy,reverse
from django.views.generic import View, CreateView
from shop.models import Category,Subcategory,Product,ProductImage
from django.core.mail import send_mail
from django.contrib import messages
from shop.models import CustomUser
from django.contrib.auth import authenticate,login,logout

from shop.forms import CategoryForm
from shop.forms import SubCategoryForm
from shop.forms import ProductForm
from shop.forms import ProductImageForm


# Create your views here.
class CategoryView(View):
    def get(self,request):
        c=Category.objects.all()
        return render(request,'categories.html',{'categories':c})




class SubCategory(View):
    def get(self,request,i):
        category=get_object_or_404(Category,id=i)
        sub=category.subcategories.all()
        return render(request,'subcat.html',{'subcategories':sub})



class ProductView(View):
    def get(self,request,i):
        s=get_object_or_404(Subcategory,id=i)
        pro=Product.objects.filter(subcategory=s)
        return render(request,'product.html',{'product':pro})



class ProductDetailView(View):
    def get(self, request, i):
        product = get_object_or_404(Product, id=i)
        images = ProductImage.objects.filter(product=product)
        return render(request, 'productdetail.html', {'product': product,'images':images})


from shop.forms import SignupForm
class Signup(View):
    def post(self,request):
        form_instance=SignupForm(request.POST)
        if form_instance.is_valid():
            user=form_instance.save(commit=False) #After otp verification it will set to true
            user.is_active=False
            user.save()
            user.generate_otp()
            send_mail(
                "Ecommerce OTP",
                user.otp,
                "renjithak19@gmail.com",
                [user.email],
                fail_silently=False,
            )
            return redirect('shop:verify')
        return render(request, 'signup.html', {'form': form_instance})

    def get(self,request):
        form_instance=SignupForm()
        return render(request,'signup.html',{'form':form_instance})



class OtpVerification(View):
    def post(self,request):
        otp=request.POST.get('otp')
        try:
            u=CustomUser.objects.get(otp=otp)
            u.is_active=True
            u.is_verified=True
            u.otp=None
            u.save()
            return redirect('shop:signin')
        except:
            messages.error(request,"Invalid OTP")
            return redirect('shop:verify')

    def get(self,request):
        return render(request,'otp_verify.html')


from shop.forms import LoginForm
class Signin(View):
    def get(self,request):
        form_instance=LoginForm()
        return render(request,'signin.html',{'form':form_instance})

    def post(self,request):
        form_instance=LoginForm(request.POST)
        if form_instance.is_valid():
            name=form_instance.cleaned_data['username']
            pwd=form_instance.cleaned_data['password']
            user=authenticate(username=name,password=pwd)
            if user and user.is_superuser==True:
                login(request,user)
                return redirect('shop:home')
            elif user and user.is_superuser==False:
                login(request,user)
                return redirect('shop:home')
            else:
                print("Invalid User Credentials")
                return redirect('signin')


class Signout(View):
    def get(self,request):
        logout(request)
        return redirect('shop:signin')


#
# class Add_category(View):
#     def get(self,request):
#         form_instance=CategoryForm()
#         return render(request,'addcategories.html',{'form':form_instance})
#     def post(self,request):
#         form_instance=CategoryForm(request.POST,request.FILES)
#         if form_instance.is_valid():
#             form_instance.save()
#             return redirect('shop:home')
#         return render(request,'addcategories.html',{'form':form_instance})
#
#
#
# class Add_subcategory(View):
#     def get(self,request):
#         form_instance=SubCategoryForm()
#         return render(request,'addsubcategory.html',{'form':form_instance})
#
#     def post(self,request):
#         form_instance=SubCategoryForm(request.POST,request.FILES)
#         if form_instance.is_valid():
#             form_instance.save()
#             return redirect('shop:sub')
#         return render(request, 'addsubcategory.html', {'form': form_instance})
#
#
# class Add_Product(View):
#     def get(self,request):
#         form_instance=ProductForm()
#         return render(request,'addproduct.html',{'form':form_instance})
#
#     def post(self,request):
#         form_instance=ProductForm(request.POST,request.FILES)
#         if form_instance.is_valid():
#             form_instance.save()
#             return redirect('shop:sub')
#         return render(request, 'addproduct.html', {'form': form_instance})
#
#
# class Add_Image(View):
#     def get(self,request):
#         form_instance=ProductImageForm()
#         return render(request,'productimage.html',{'form':form_instance})
#
#     def post(self,request):
#         form_instance=ProductImageForm(request.POST,request.FILES)
#         if form_instance.is_valid():
#             form_instance.save()
#             return redirect('shop:sub')
#         return render(request, 'productimage.html', {'form': form_instance})


class Add_category(CreateView):
    model=Category
    form_class = CategoryForm
    template_name = 'addcategories.html'
    success_url = reverse_lazy('shop:home')

class Add_subcategory(CreateView):
    model = Subcategory
    form_class = SubCategoryForm
    template_name = 'addsubcategory.html'


    def get_success_url(self):
        return reverse(
            'shop:sub',
            kwargs={'i':self.object.category.id}
        )

class Add_Product(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'addproduct.html'


    def get_success_url(self):
        return reverse(
            'shop:prod',
            kwargs={'i':self.object.subcategory.id}
        )

class Add_Image(CreateView):
    model = ProductImage
    form_class = ProductImageForm
    template_name = 'productimage.html'


    def get_success_url(self):
        return reverse(
            'shop:detail',
            kwargs={'i':self.object.product.id}
        )


#
