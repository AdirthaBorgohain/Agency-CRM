from django.db import models
from datetime import datetime

# Create your models here.


CATEGORY_CHOICES = (
    ("Newspaper", "Newspaper"),
    ("Magazine", "Magazine")
)

LANGUAGE_CHOICES = (
    ("Assamese", "Assamese"),
    ("English", "English"),
    ("Hindi", "Hindi"),
    ("Bengali", "Bengali"),
    ("Others", "Others")
)


class Customer(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.name


class Agent(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=12, unique=True)
    commission = models.FloatField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=20, unique=True)
    language = models.CharField(
        max_length=10, choices=LANGUAGE_CHOICES, default="Assamese")
    category = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES, default="Newspaper")
    price = models.FloatField()

    def __str__(self):
        return self.name


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    create_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    additional_charges = models.FloatField(default=0)
    grand_total = models.FloatField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.name + " (" + str(self.start_date.strftime("%B")) + ")"

    @property
    def bill_period(self):
        return '{} -- {}'.format(self.start_date.strftime("%d/%m/%Y"), self.end_date.strftime("%d/%m/%Y"))


class Bill(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    create_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    deductions = models.FloatField(default=0)
    prev_balance = models.FloatField()
    grand_total = models.FloatField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.agent.name + " (" + str(self.start_date.strftime("%B")) + ")"

    @property
    def bill_period(self):
        return '{} -- {}'.format(self.start_date.strftime("%d/%m/%Y"), self.end_date.strftime("%d/%m/%Y"))


class OrderDetails(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.FloatField()
    net_price = models.FloatField()

    def __str__(self):
        return self.invoice.customer.name + " (" + str(self.invoice.start_date.strftime("%B")) + ")-" + self.product.name

class BillDetails(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.FloatField()
    net_price = models.FloatField()

    def __str__(self):
        return self.bill.agent.name + " (" + str(self.bill.start_date.strftime("%B")) + ")-" + self.product.name
