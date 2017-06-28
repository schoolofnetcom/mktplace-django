from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from billing.forms import PaymentForm, EditOrderForm
from billing.models import Order
from billing.services import BillingService
from portal.models import Product


@login_required
def payment(request, product_id):
    context = {}
    product = get_object_or_404(Product, pk=product_id)
    form = PaymentForm()
    context['product'] = product
    context['form'] = form

    user = request.user

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            full_name = request.POST.get('first_name').split(' ', 1)
            card_data = {
                'description': 'Market Place Payment',
                'item_type': 'credit_card',
                'data': {
                    'number': form.cleaned_data['number'],
                    'verification_value': form.cleaned_data['verification_value'],
                    'first_name': full_name[0],
                    'last_name': full_name[1],
                    'month': form.cleaned_data['month'],
                    'year': form.cleaned_data['year']
                }
            }

            context['form'] = form
            order = BillingService().charge(user, product, card_data)
            if order:
                return redirect('billing_item_purchased', order.id)

            context['error'] = True

    return render(request, 'billing/payment.html', context)


@login_required
def item_purchased(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if order.user != request.user:
        return redirect('home')

    context = {
        'order': order
    }

    return render(request, 'billing/item_purchased.html', context)


@login_required
def my_orders(request):
    orders = Order.objects.filter(merchant=request.user)

    context = {
        'orders': orders
    }

    return render(request, 'billing/my_orders.html', context)


@login_required
def sales(request):
    orders = Order.objects.filter(merchant=request.user, status='Approved')

    context = {
        'orders': orders
    }

    return render(request, 'billing/sales.html', context)


@login_required
def change_shipment_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if order.user != request.user:
        return redirect('home')

    form = EditOrderForm(instance=order)

    if request.method == 'POST':
        form = EditOrderForm(request.POST)
        if form.is_valid():
            order.shipment_status = form.cleaned_data['shipment_status']
            order.save()
            return redirect('billing_sales')

    context = {
        'form': form,
        'order': order
    }

    return render(request, 'billing/change_shipment_status.html', context)
