from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import Product, ProductVariation  # Update this import
from .forms import ProductVariationForm, ProductForm  # Assuming you've renamed or updated the form
from django.contrib import messages
from django.urls import reverse_lazy

# Create your views here.
def index(request):
    # Render index.html
    return render( request, 'aintdoinit/index.html')


class ProductListView(generic.ListView):
    model = Product
    
class ProductDetailView(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        # Get the product object for this view
        product = self.get_object()
        # Filter the variations based on the specific product
        variation_list = ProductVariation.objects.filter(product=product)
        context['variation_list'] = variation_list
        return context
    
    
def createProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('product-detail', product.id)
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'aintdoinit/product_form.html', context)

def updateProduct(request, product_id):
    product = Product.objects.get(pk=product_id) 
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            updated_product = form.save()
            return redirect('product-list')
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'product_id': product_id}
    return render(request, 'aintdoinit/product_form.html', context)

def deleteProduct(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product-list')
    
    context = {'product': product}
    return render(request, 'aintdoinit/product_delete.html', context)    
    


class VariationListView(generic.ListView):
    model = ProductVariation

class VariationDetailView(generic.DetailView):
    model = ProductVariation

def createVariation(request, product_id):
    form = ProductVariationForm()  # Updated this
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        form = ProductVariationForm(request.POST)
        if form.is_valid():
            variation = form.save(commit=False)
            variation.product = product
            variation.save()  # Save the variation instance
            return redirect('product-detail', product_id)

    context = {'form': form, 'product_id': product_id}
    return render(request, 'aintdoinit/variation_form.html', context)  # Updated the template name (you should rename your template too)

def updateVariation(request, product_id, variation_id):
    variation = ProductVariation.objects.get(pk=variation_id)
    
    if request.method == 'POST':
        form = ProductVariationForm(request.POST, instance=variation)
        if form.is_valid():
            updated_variation = form.save()
            return redirect('product-detail', product_id)
    else:
        form = ProductVariationForm(instance=variation)
    
    context = {'form': form, 'product_id': product_id, 'variation_id': variation_id}
    return render(request, 'aintdoinit/variation_form.html', context)  # Adjusted template name

def deleteVariation(request, product_id, variation_id):
    variation = ProductVariation.objects.get(pk=variation_id)
    product = Product.objects.get(pk=product_id)
    
    if request.method == 'POST':
        variation.delete()
        return redirect('product-detail', product_id)
    
    return render(request, 'aintdoinit/variation_delete.html', {'variation': variation, 'product': product})  # Adjusted template name


def toggle_dark_mode(request):
    current_mode = request.session.get('dark_mode', False)
    print("Current dark mode status:", current_mode)  # Debug line
    request.session['dark_mode'] = not current_mode
    return redirect(request.META.get('HTTP_REFERER', 'default_url_if_no_referer'))