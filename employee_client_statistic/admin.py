from django.contrib import admin
from employee_client_statistic.models import Employee, Order, Product, Client

admin.site.register((Employee, Order, Product, Client))
