from customer.models import Customer


def filter_customers(mailing):
    customers = Customer.objects.filter(
        operator_code=mailing.filter_field.operator_code,
        tag=mailing.filter_field.tag
    )
    return customers
