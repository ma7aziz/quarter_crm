from .models import Customer


def add_customer(phone, name, *email):
    customer = Customer(name=name, phone=phone)
    customer.save()
    if email:
        customer.email = email
        customer.save()
    return customer
