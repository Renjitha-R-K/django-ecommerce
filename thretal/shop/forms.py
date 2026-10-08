
from django import forms
from django.contrib.auth.models import User

from shop.models import CustomUser,Category,Subcategory,Product,ProductImage
from django.contrib.auth.forms import UserCreationForm
class SignupForm(UserCreationForm):

    class Meta:
        model=CustomUser
        fields=['username','password1','password2','email','first_name','last_name','phone']




class LoginForm(forms.Form):

    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)



class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name','image']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model=Subcategory
        fields=['category','name','description','image']


class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields = [
            'subcategory', 'name', 'description', 'price', 'stock',
            'brand', 'size', 'color', 'material', 'is_best_seller', 'image'
        ]

class ProductImageForm(forms.ModelForm):
    class Meta:
        model=ProductImage
        fields=['product','image']