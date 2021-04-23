from .models import Customer


def add_customer(phone, name, *email):
    customer = Customer.objects.all().filter(phone=phone).first()
    if not customer:
        customer = Customer(name=name, phone=phone)
        customer.save()
        if email:
            customer.email = email
            customer.save()
    print(customer)
    return customer
