from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from portal.forms import ProductForm
from portal.models import Product, Category


def home(request):
    return render(request, 'portal/home.html', {})


def my_products(request):
    products = Product.objects.filter(user=request.user)

    context = {
        'products': products
    }

    return render(request, 'portal/my_products.html', context)


def product_new(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = Product()
            product.user = request.user
            product.name = form.cleaned_data['name']
            product.quantity = form.cleaned_data['quantity']
            product.price = form.cleaned_data['price']
            product.short_description = form.cleaned_data['short_description']
            product.description = form.cleaned_data['description']
            product.status = 'Active'
            product.save()

            categories = Category.objects.filter(id__in=request.POST.getlist('categories'))
            if categories:
                for category in categories:
                    product.categories.add(category)

            return redirect('my_products')

    form = ProductForm()

    context = {
        'form': form,
    }

    return render(request, 'portal/product_new.html', context)


def product_edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if product.user != request.user:
        return HttpResponseForbidden

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.quantity = form.cleaned_data['quantity']
            product.price = form.cleaned_data['price']
            product.short_description = form.cleaned_data['short_description']
            product.description = form.cleaned_data['description']
            product.categories = form.cleaned_data['categories']
            product.status = form.cleaned_data['status']

            product.save()
            return redirect('my_products')

    form = ProductForm(instance=product)

    context = {
        'product': product,
        'form': form,
    }

    return render(request, 'portal/product_edit.html', context)
