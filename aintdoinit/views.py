from django.shortcuts import render, redirect, get_object_or_404
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
    context_object_name = 'products_by_type'  # this is how you'll access the data in the template
    template_name = 'your_template_name.html'  # specify your template name if it's not the default

    def get_queryset(self):
        # Filtering by product type
        product_type = self.request.GET.get('product_type')
        if product_type:
            queryset = Product.objects.filter(product_type=product_type)
        else:
            queryset = Product.objects.all()
    
        # Sorting by price
        price_sort = self.request.GET.get('price_sort')
        if price_sort == "asc":
            queryset = queryset.order_by('price', 'product_type', 'title')
        elif price_sort == "desc":
            queryset = queryset.order_by('-price', 'product_type', 'title')
        else:
            queryset = queryset.order_by('product_type', 'title')
    
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_by_type = {display_name: [] for _, display_name in Product.PRODUCT_TYPE}

        for product in self.get_queryset():
            display_name = dict(Product.PRODUCT_TYPE)[product.product_type]
            products_by_type[display_name].append(product)

        # If a filter is applied, only keep that category in the context
        selected_product_type = self.request.GET.get('product_type')
        if selected_product_type:
            selected_display_name = dict(Product.PRODUCT_TYPE)[selected_product_type]
            context['products_by_type'] = {selected_display_name: products_by_type[selected_display_name]}
        else:
            # Only retain categories that have products
            context['products_by_type'] = {key: value for key, value in products_by_type.items() if value}

        context['PRODUCT_TYPE'] = Product.PRODUCT_TYPE 
        return context
    
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
            return redirect('products')
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'product_id': product_id}
    return render(request, 'aintdoinit/product_form.html', context)

def deleteProduct(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    
    context = {'product': product}
    return render(request, 'aintdoinit/product_delete.html', context)    
    


class VariationListView(generic.ListView):
    model = ProductVariation

class VariationDetailView(generic.DetailView):
    model = ProductVariation

def createVariation(request, product_id):
    product = get_object_or_404(Product, pk=product_id)  # safer retrieval
    form = ProductVariationForm()

    if request.method == 'POST':
        form = ProductVariationForm(request.POST)
        if form.is_valid():
            variation = form.save(commit=False)
            variation.product = product
            variation.save()
            return redirect('product-detail', product_id)

    context = {'form': form, 'product_id': product_id}
    return render(request, 'aintdoinit/variation_form.html', context)

def updateVariation(request, product_id, variation_id):
    variation = get_object_or_404(ProductVariation, pk=variation_id)  # safer retrieval

    if request.method == 'POST':
        form = ProductVariationForm(request.POST, instance=variation)
        if form.is_valid():
            form.save()
            return redirect('product-detail', product_id)
    else:
        form = ProductVariationForm(instance=variation)

    context = {'form': form, 'product_id': product_id, 'variation_id': variation_id}
    return render(request, 'aintdoinit/variation_form.html', context)

def deleteVariation(request, product_id, variation_id):
    variation = get_object_or_404(ProductVariation, pk=variation_id)  # safer retrieval
    product = get_object_or_404(Product, pk=product_id)  # safer retrieval

    if request.method == 'POST':
        variation.delete()
        return redirect('product-detail', product_id)

    return render(request, 'aintdoinit/variation_delete.html', {'variation': variation, 'product': product})

def toggle_dark_mode(request):
    current_mode = request.session.get('dark_mode', False)
    print("Current dark mode status:", current_mode)  # Debug line
    request.session['dark_mode'] = not current_mode
    return redirect(request.META.get('HTTP_REFERER', 'default_url_if_no_referer'))