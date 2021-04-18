import simplejson as json
from entities.models import Customer, Agent, Product, Invoice, Bill, OrderDetails, BillDetails
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    invoices = Invoice.objects.order_by('-create_date')
    bills = Bill.objects.order_by('-create_date')
    products = Product.objects.order_by('name')
    data_object = {"invoices": invoices, "bills": bills, "products": products}
    return render(request, "home.html", {"data": data_object})

@login_required
def analytics(request):
    bills = Bill.objects.all()
    invoices = Invoice.objects.all()
    total_paid_bill, total_unpaid_bill = 0, 0
    total_paid_invoice, total_unpaid_invoice = 0, 0
    for bill in bills:
        if bill.is_paid == True:
            total_paid_bill += bill.grand_total
        else:
            total_unpaid_bill += bill.grand_total
    for invoice in invoices:
        if invoice.is_paid == True:
            total_paid_invoice += invoice.grand_total
        else:
            total_unpaid_invoice += invoice.grand_total

    data_object = {
        "bill": {
            "total_paid": total_paid_bill,
            "total_unpaid": total_unpaid_bill
        },
        "invoice": {
            "total_paid": total_paid_invoice,
            "total_unpaid": total_unpaid_invoice,
        }
    }
    return render(request, "analytics.html", {"data": data_object})

@login_required
def customers_agents(request):
    customers = Customer.objects.order_by('name')
    agents = Agent.objects.order_by('name')

    data_object = {
        "agents": agents,
        "customers": customers
    }
    return render(request, "customers.html", {"data": data_object})

