import simplejson as json
from datetime import date
from .models import Customer, Agent, Product, Invoice, Bill, OrderDetails, BillDetails
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView

# Create your views here.


@login_required
def add_customer(request):
    if request.method == 'POST':
        print('RECEIVED REQUEST: ' + request.method)
        data = json.loads(request.body.decode('utf-8'))
        customer_id = data.get("customer_id")
        name = data.get("name")
        address = data.get("address")
        contact = data.get("contact")
        customer_type = data.get("customer_type")
        commission = data.get("commission")
        if customer_type == "Customer":
            new_customer = Customer(id=customer_id, name=name, 
                                    address=address, contact=contact)
            new_customer.save()
        elif customer_type == "Agent":
            new_agent = Agent(id=customer_id, name=name, address=address,
                              contact=contact, commission=commission)
            new_agent.save()
        return HttpResponse(json.dumps({"customer_type": customer_type}))
    else:
        return render(request, 'customer_creation.html')


@login_required
def add_product(request):
    if request.method == 'POST':
        print('RECEIVED REQUEST: ' + request.method)
        data = json.loads(request.body.decode('utf-8'))
        name = data.get("name")
        language = data.get("language")
        price = data.get("price")
        category = data.get("category")
        new_product = Product(name=name, language=language,
                              price=price, category=category)
        new_product.save()
        return HttpResponse("Product Added...")
    else:
        return render(request, 'product_creation.html')


@login_required
def create_bill(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        agent_id = data.get("agent")
        start_date = data.get("startDate")
        end_date = data.get("endDate")
        product_ids = data.get("products")
        quantities = data.get("quantities")
        deductions = float(data.get("deductions"))
        prev_balance = data.get("prevBalance")
        date_today = date.today()
        print("start_date: ", start_date)
        product_prices = list()
        for product_id in product_ids:
            product = Product.objects.get(pk=product_id)
            product_prices.append(product.price)
        sub_total = 0
        for quantity, product_price in zip(quantities, product_prices):
            sub_total += int(quantity)*float(product_price)
        net_total = sub_total - float(deductions)
        grand_total = net_total + float(prev_balance)
        bill = Bill(agent_id=agent_id, start_date=start_date, end_date=end_date,
                    deductions=deductions, prev_balance=prev_balance, grand_total=grand_total, create_date=date_today)
        bill.save()
        for product_id, product_price, quantity in zip(product_ids, product_prices, quantities):
            order_details = BillDetails(bill_id=bill.id, product_id=product_id, quantity=quantity,
                                        price=product_price, net_price=float(product_price)*int(quantity))
            order_details.save()
        return HttpResponse("Bill Generated...")
    else:
        registered_agents = Agent.objects.all()
        registered_products = Product.objects.all()
        price_dict, commission_dict = dict(), dict()
        for product in registered_products:
            price_dict[product.id] = product.price
        for agent in registered_agents:
            commission_dict[agent.id] = agent.commission
        date_today = date.today()
        data_object = {
            "customers": registered_agents,
            "products": registered_products,
            "price_dict": json.dumps(price_dict),
            "commission_dict": json.dumps(commission_dict),
            "date_today": date_today,
            "customer_type": "Agent"
        }
        return render(request, "invoice_creation.html", {"data": data_object})


@login_required
def create_invoice(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        customer_id = data.get("customer")
        start_date = data.get("startDate")
        end_date = data.get("endDate")
        product_ids = data.get("products")
        quantities = data.get("quantities")
        add_charges = data.get("addCharge")
        print("start_date: ", start_date)
        date_today = date.today()
        product_prices = list()
        for product_id in product_ids:
            # Product.objects.filter(language="Assamese")
            product = Product.objects.get(pk=product_id)
            product_prices.append(product.price)
        total_amount = 0
        for quantity, product_price in zip(quantities, product_prices):
            total_amount += int(quantity)*float(product_price)
        total_amount += float(add_charges)
        invoice = Invoice(customer_id=customer_id, start_date=start_date,
                          end_date=end_date, additional_charges=add_charges, grand_total=total_amount, create_date=date_today)
        invoice.save()
        for product_id, product_price, quantity in zip(product_ids, product_prices, quantities):
            order_details = OrderDetails(invoice_id=invoice.id, product_id=product_id, quantity=quantity,
                                         price=product_price, net_price=float(product_price)*int(quantity))
            order_details.save()
        return HttpResponse("Invoice Generated...")
    else:
        registered_customers = Customer.objects.all()
        registered_products = Product.objects.all()
        price_dict = dict()
        for product in registered_products:
            price_dict[product.id] = product.price
        date_today = date.today()
        data_object = {
            "customers": registered_customers,
            "products": registered_products,
            "price_dict": json.dumps(price_dict),
            "date_today": date_today,
            "customer_type": "Customer"
        }
        return render(request, "invoice_creation.html", {"data": data_object})

@login_required
def autogenerate_invoice(request, customer_id):
    if request.method == 'POST':
        print("AUTOGENERATING INVOICE FOR CUSTOMER ID: ", customer_id)
        recent_invoice = Invoice.objects.filter(customer_id=customer_id).latest("end_date")
        products = OrderDetails.objects.filter(invoice_id=recent_invoice).values_list('product', flat=True)
        hawker_charges = recent_invoice.additional_charges
        products = list(products)
        return HttpResponse(json.dumps({"products": products, "hawker_charges": hawker_charges}))

@login_required
def invoice_details(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    customer = invoice.customer
    order_details = OrderDetails.objects.filter(invoice_id=invoice_id)
    invoice.sub_total = invoice.grand_total - invoice.additional_charges
    # print(invoice.sub_total)
    data_object = {
        "invoice": invoice,
        "customer": customer,
        "order_details": order_details,
        "customer_type": "Customer"
    }
    return render(request, "invoice_details.html", {"data": data_object})


@login_required
def bill_details(request, bill_id):
    bill = Bill.objects.get(id=bill_id)
    agent = bill.agent
    bill_details = BillDetails.objects.filter(bill_id=bill_id)
    bill.net_total = bill.grand_total - bill.prev_balance
    bill.sub_total = bill.net_total + bill.deductions
    data_object = {
        "invoice": bill,
        "customer": agent,
        "order_details": bill_details,
        "customer_type": "Agent"
    }
    return render(request, "invoice_details.html", {"data": data_object})


@login_required
def delete_invoice(request, invoice_id):
    print("INVOICE ID TO BE DELETED: ", invoice_id)
    Invoice.objects.filter(id=invoice_id).delete()
    return HttpResponse("Invoice Deleted...")


@login_required
def delete_bill(request, bill_id):
    print("BILL ID TO BE DELETED: ", bill_id)
    Bill.objects.filter(id=bill_id).delete()
    return HttpResponse("Bill Deleted...")


@login_required
def change_payment_status(request):
    data = json.loads(request.body.decode('utf-8'))
    # print("DATA: ", data)
    invoice_id = data.get("invoice_id")
    payment_status = data.get("payment_status")
    if data.get("customer_type") == "Agent":
        if payment_status == "Completed":
            Bill.objects.filter(id=invoice_id).update(is_paid=True)
        else:
            Bill.objects.filter(id=invoice_id).update(is_paid=False)
    else:
        if payment_status == "Completed":
            Invoice.objects.filter(id=invoice_id).update(is_paid=True)
        else:
            Invoice.objects.filter(id=invoice_id).update(is_paid=False)
    return HttpResponse(json.dumps({"status": "ok"}))

@login_required
def agent_details(request, agent_id):
    if request.method == 'GET':
        agent_id = agent_id.replace('__','/')
        agent = Agent.objects.get(pk=agent_id)
        bills = Bill.objects.filter(agent_id=agent_id)
        data_object = {
        "customer": agent,
        "invoices": bills,
        "customer_type": "Agent"
    }
    return render(request, "customer_details.html", {"data": data_object})

@login_required
def delete_agent(request, agent_id):
    print("AGENT ID TO BE DELETED: ", agent_id)
    Agent.objects.filter(id=agent_id).delete()
    return HttpResponse("Agent Deleted...")


@login_required
def customer_details(request, customer_id):
    if request.method == 'GET':
        customer_id = customer_id.replace('__','/')
        customer = Customer.objects.get(pk=customer_id)
        invoices = Invoice.objects.filter(customer_id=customer_id)
        data_object = {
        "customer": customer,
        "invoices": invoices,
        "customer_type": "Customer"
    }
    return render(request, "customer_details.html", {"data": data_object})

@login_required
def delete_customer(request, customer_id):
    print("CUSTOMER ID TO BE DELETED: ", customer_id)
    Customer.objects.filter(id=customer_id).delete()
    return HttpResponse("Customer Deleted...")

@login_required
def update_customer(request):
    print('RECEIVED REQUEST: ' + request.method)
    data = json.loads(request.body.decode('utf-8'))
    customer_id = data.get("customer_id")
    name = data.get("name")
    address = data.get("address")
    contact = data.get("contact")
    customer_type = data.get("customer_type")
    commission = data.get("commission")
    if customer_type == "Customer":
        existing_customer = Customer.objects.filter(pk=customer_id).update(name=name, address=address, contact=contact)
        print("UPDATED AND SAVED CUSTOMER")
    elif customer_type == "Agent":
        existing_agent = Agent.objects.filter(pk=customer_id).update(name=name, address=address, contact=contact, commission=commission)
        print("UPDATED AND SAVED AGENT")
    return HttpResponse(json.dumps({"status": "ok"}))
