"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from Customer.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/create-customer/', create_customer, name='create-customer'),
    path('api/customers/',list_customers, name='list-customers'),
    path('api/customers/<int:pk>/', retrieve_customer, name='retrieve-customer'),
    path('api/customers/<int:pk>/update/', update_customer, name='update_customer'),  # URL for updating a customer
    path('api/create-contact/', create_contact, name='create-contact'),
    path('api/contacts/', list_contacts, name='list-contacts'),
    path('api/contacts/<int:pk>/', retrieve_contact, name='retrieve-contact'),
    path('api/customer_contact/<customer_id>/',customer_contact,name='customer_contact'),
    path('api/customer_contact/<customer_id>/update/',update_customer_contact,name='update_customer_contact')
]
