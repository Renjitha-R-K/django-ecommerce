"""
URL configuration for thretal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
app_name="shop"
urlpatterns = [
    path('',views.CategoryView.as_view(),name='home'),
    path('sub/<int:i>',views.SubCategory.as_view(),name='sub'),
    path('prod/<int:i>',views.ProductView.as_view(),name='prod'),
    path('detail/<int:i>',views.ProductDetailView.as_view(),name='detail'),
    path('signup',views.Signup.as_view(),name='signup'),
    path('verify',views.OtpVerification.as_view(),name='verify'),
    path('signin',views.Signin.as_view(),name='signin'),
    path('signout',views.Signout.as_view(),name='signout'),
    path('addcat',views.Add_category.as_view(),name='addcat'),
    path('addsub',views.Add_subcategory.as_view(),name='addsub'),
    path('addpro',views.Add_Product.as_view(),name='addpro'),
    path('proimage',views.Add_Image.as_view(),name='proimage'),

]

