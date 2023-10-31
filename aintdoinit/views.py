from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import Product,Mod
from .forms import ModForm, ProductForm
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
        # Filter the mods based on the specific product and active status
        mod_list = Mod.objects.filter(product=product, product__is_active=True)
        context['mod_list'] = mod_list

        return context


class ProjectListView(generic.ListView):
    model = Mod
class ProjectDetailView(generic.DetailView):
    model = Mod


def createMod(request, product_id):
    form = ModForm()
    product = Product.objects.get(pk=product_id)
    
    if request.method == 'POST':
        form = ModForm(request.POST)
        if form.is_valid():
            mod = form.save(commit=False)
            mod.product = product
            mod.save()
            return redirect('product-detail', product_id)

    context = {'form': form, 'product_id': product_id}
    return render(request, 'aintdoinit/mod_form.html', context)

def updateMod(request, product_id, mod_id):
    mod = Mod.objects.get(pk=mod_id)
    if request.method == 'POST':
        form = ModForm(request.POST, instance=mod)
        if form.is_valid():
            updated_mod = form.save()
            return redirect('product-detail', product_id)
    else:
        form = ModForm(instance=mod)
    context = {'form': form, 'product_id': product_id, 'mod_id': mod_id}
    return render(request, 'aintdoinit/mod_form.html', context)

def deleteMod(request, product_id, mod_id):

    mod = Mod.objects.get(pk=mod_id)
    product = Product.objects.get(pk=product_id) 
    if request.method == 'POST':
        mod.delete()
        #redirect back to product detail after delete
        return redirect('product-detail', product_id)
    #handle GET request by going to confirmation page
    return render(request, 'aintdoinit/mod_delete.html', {'mod': mod, 'product': product})

def createProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # request.FILES added for handling image uploads
        if form.is_valid():
            product = form.save()
            return redirect('product-detail', product.id)  # Redirect to the detail page of the newly created product
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'aintdoinit/product_form.html', context)

def updateProduct(request, product_id):
    #fetch the existing project object
    product = Product.objects.get(pk=product_id) 
    if request.method == 'POST':
        #pre-fill the form with the existing data
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            #save the updated form data
            updated_product = form.save()
            #redirect back to the product list page
            return redirect('product-list')
    else:
        #create a form pre-filled with the existing data
        form = ProductForm(instance=product)
    context = {'form': form,'product_id': product_id,}
    return render(request, 'aintdoinit/product_form.html', context)

def deleteProduct(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product-list')  # Redirect back to the list of all products
    
    context = {'product': product}
    return render(request, 'aintdoinit/product_delete.html', context)


def toggle_dark_mode(request):
    current_mode = request.session.get('dark_mode', False)
    print("Current dark mode status:", current_mode)  # Debug line
    request.session['dark_mode'] = not current_mode
    return redirect(request.META.get('HTTP_REFERER', 'default_url_if_no_referer'))