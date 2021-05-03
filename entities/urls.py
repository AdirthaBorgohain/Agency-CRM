from . import views
from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path("add_customer", views.add_customer, name="add_customer"),
    path("update_customer", views.update_customer, name="update_customer"),
    path("add_product", views.add_product, name="add_product"),
    path("create_bill", views.create_bill, name="create_bill"),
    path("create_invoice", views.create_invoice, name="create_invoice"),
    path("bill/view/<int:bill_id>/", views.bill_details, name="bill_page"),
    path("bill/delete/<int:bill_id>", views.delete_bill, name="delete_bill"),
    path("invoice/view/<int:invoice_id>/", views.invoice_details, name="invoice_page"),
    path("invoice/delete/<int:invoice_id>", views.delete_invoice, name="delete_invoice"),
    path("invoice/autogenerate/<str:customer_id>", views.autogenerate_invoice, name="autogenerate_invoice"),
    path('update_payment_status',views.change_payment_status,name="change_payment_status"),
    path("agent/view/<str:agent_id>", views.agent_details, name="agent_details"),
    path("agent/delete/<str:agent_id>", views.delete_agent, name="delete_agent"),
    path("customer/view/<str:customer_id>", views.customer_details, name="customer_details"),
    path("customer/delete/<str:customer_id>", views.delete_customer, name="delete_customer"),
    path("generate_upi_link", views.generate_upi_link, name="generate_upi_link"),
    path("add_payment", views.add_payment, name="add_payment")
    ]