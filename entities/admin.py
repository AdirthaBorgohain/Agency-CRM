from django.contrib import admin
from .models import Customer, Agent, Product, Invoice, Bill, OrderDetails, BillDetails

# Register your models here.
admin.site.register(Customer)
admin.site.register(Agent)
admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(Bill)
admin.site.register(OrderDetails)
admin.site.register(BillDetails)