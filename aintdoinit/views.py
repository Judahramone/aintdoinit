from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import generic
from .models import Product, Size, Color, ProductVariation, Cart, CartItem, Customer
from .forms import ProductVariationForm, ProductForm, CreateUserForm 
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .constants import COLOR_CSS_MAP
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
#from .decorators import allowed_users
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_superuser  # or use user.has_perm('some_permission') for specific permissions

# Create your views here.
def index(request):
    # Render index.html
    return render( request, 'aintdoinit/index.html')

def passwordReset(request):
    # Render index.html
    return render( request, 'registration/password_reset_form.html')

class ProductListView(generic.ListView):
    model = Product
    context_object_name = 'products_by_type' 

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
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        enable_add_to_cart=False

        # Initialize size_ids and color_ids to ensure they have a value
        size_ids = []
        color_ids = []

        # Fetch all available sizes for this product
        size_ids = ProductVariation.objects.filter(product=product, stock__gt=0) \
                                           .values_list('size__id', flat=True) \
                                           .distinct().order_by('size__id')

        # Now that we have size_ids, we can get the Size objects
        available_sizes = Size.objects.filter(id__in=size_ids)

        # Similar for colors
        color_ids = ProductVariation.objects.filter(product=product, stock__gt=0) \
                                            .values_list('color__id', flat=True) \
                                            .distinct()
        available_colors = Color.objects.filter(id__in=color_ids)

        variation_list = ProductVariation.objects.filter(product=product).order_by('size', 'color')
        
        # Get selected size and color from request
        selected_color = self.request.GET.get('color', None)
        selected_size = self.request.GET.get('size', None)
        
        # Determine if 'Add to Cart' should be enabled
        if selected_color and selected_size:
            matching_variation = ProductVariation.objects.filter(
            product=product,
            color_id=selected_color,
            size_id=selected_size,
            stock__gt=0
            )
            if matching_variation.exists():
                enable_add_to_cart = True

        context.update({
            'product': product,
            'available_sizes': available_sizes,
            'available_colors': available_colors,
            'selected_color': selected_color,
            'selected_size': selected_size,
            'enable_add_to_cart': enable_add_to_cart,
            'variation_list': variation_list,
        })

        return context

@login_required
@user_passes_test(is_admin)  
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

@login_required
@user_passes_test(is_admin)  
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

@login_required
@user_passes_test(is_admin)  
def deleteProduct(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    
    context = {'product': product}
    return render(request, 'aintdoinit/product_delete.html', context)    
    

class VariationListView(LoginRequiredMixin, generic.ListView):
    model = ProductVariation

class VariationDetailView(LoginRequiredMixin, generic.DetailView):
    model = ProductVariation

@login_required
@user_passes_test(is_admin)  
def updateVariation(request, product_id, variation_id):
    variation = get_object_or_404(ProductVariation, pk=variation_id)
    
    # Check if we have stock to append from the session
    append_stock = request.session.pop('append_stock', None)
    
    form = ProductVariationForm(request.POST or None, instance=variation)
    
    if request.method == 'POST' and form.is_valid():
        if append_stock:
            # Append the stock instead of just saving the form
            variation.stock += append_stock
            variation.save()
        else:
            form.save()
        return redirect('product-detail', product_id)
    elif append_stock:
        # Prepopulate the form with the appended stock
        variation.stock += append_stock
        form = ProductVariationForm(instance=variation)

    context = {'form': form, 'product_id': product_id, 'variation_id': variation_id}
    return render(request, 'aintdoinit/variation_form.html', context)

@login_required
@user_passes_test(is_admin)  
def createVariation(request, product_id):
    product = get_object_or_404(Product, pk=product_id)  # safer retrieval
    form = ProductVariationForm()

    if request.method == 'POST':
        form = ProductVariationForm(request.POST)
        if form.is_valid():
            # Extract the necessary data to check for existing variation
            size = form.cleaned_data['size']
            color = form.cleaned_data['color']
            stock = form.cleaned_data['stock']
            
            # Check if variation already exists
            existing_variation = ProductVariation.objects.filter(
                product=product, size=size, color=color
            ).first()
            
            if existing_variation:
                # Instead of creating a new variation, update the existing one
                request.session['append_stock'] = stock
                return redirect('update_variation', product_id, existing_variation.id)
            else:
                variation = form.save(commit=False)
                variation.product = product
                variation.save()
                return redirect('product-detail', product_id)

    context = {'form': form, 'product_id': product_id}
    return render(request, 'aintdoinit/variation_form.html', context)

@login_required
@user_passes_test(is_admin)  
def deleteVariation(request, product_id, variation_id):
    variation = get_object_or_404(ProductVariation, pk=variation_id) 
    product = get_object_or_404(Product, pk=product_id)  

    if request.method == 'POST':
        variation.delete()
        return redirect('product-detail', product_id)

    return render(request, 'aintdoinit/variation_delete.html', {'variation': variation, 'product': product})

def toggle_dark_mode(request):
    current_mode = request.session.get('dark_mode', False)
    print("Current dark mode status:", current_mode)  #Debug line
    request.session['dark_mode'] = not current_mode
    return redirect(request.META.get('HTTP_REFERER', 'default_url_if_no_referer'))

def add_to_cart(request, product_id):
    print("POST data:", request.POST)#Debug line
    if request.method == "POST":
        selected_size = request.POST.get('selected_size')#Debug line
        selected_color = request.POST.get('selected_color')#Debug line
        print("POST size:", str(selected_size)) 
        print("POST color:", str(selected_color)) 
         # Check if both size and color are selected
        if not selected_size or not selected_color:
            return HttpResponse("Please select both a size and a color.", status=400)
        # Assuming you have unique combinations of product, size, and color
        try:
            product_variation = ProductVariation.objects.get(
                product_id=product_id,
                size_id=selected_size,
                color_id=selected_color,
                stock__gt=0
            )
            print(str(product_variation))
        except ProductVariation.DoesNotExist:
            return HttpResponse("Error: Product variation selected is not available please try an alternative selection.", status=400)

        cart_id = 1  # Fixed cart ID for testing
        cart, created = Cart.objects.get_or_create(id=cart_id)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product_variation=product_variation
        )
        if not created:
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1
        cart_item.save()

        return redirect(request.META.get('HTTP_REFERER', reverse('cart_view')))
    
def remove_from_cart(request, product_variation_id):
    cart_id = 1  # Fixed cart ID for testing
    try:
        cart = Cart.objects.get(id=cart_id)
        product_variation = ProductVariation.objects.get(id=product_variation_id)
        cart_item = CartItem.objects.get(cart=cart, product_variation=product_variation)
        cart_item.delete()
    except (CartItem.DoesNotExist, Cart.DoesNotExist, ProductVariation.DoesNotExist):
        pass  # Maybe return an error message or redirect to an error page
    return redirect('cart_view')

def increment_item(request, product_variation_id):
    cart_id = 1  # Fixed cart ID for testing
    cart = Cart.objects.get(id=cart_id)
    product_variation = ProductVariation.objects.get(id=product_variation_id)
    cart_item = CartItem.objects.get(cart=cart, product_variation=product_variation)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')

def decrement_item(request, product_variation_id):
    cart_id = 1  # Fixed cart ID for testing
    cart = Cart.objects.get(id=cart_id)
    product_variation = ProductVariation.objects.get(id=product_variation_id)
    cart_item = CartItem.objects.get(cart=cart, product_variation=product_variation)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_view')

def cart_view(request):
    cart_id = 1  # Fixed cart ID for testing
    cart, created = Cart.objects.get_or_create(id=cart_id)
    cart_items = CartItem.objects.filter(cart=cart)
    
    subtotals = {}
    grand_total = 0
    for item in cart_items:
        subtotal = item.product_variation.product.price * item.quantity
        item.subtotal = subtotal
        subtotals[item.id] = subtotal
        grand_total += subtotal

    context = {'cart_items': cart_items, 'subtotals': subtotals, 'grand_total': grand_total}
    return render(request, 'aintdoinit/cart_view.html', context)


def registerPage(request):
    form=CreateUserForm()
    if request.method=='POST':
        form= CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_day.get('username')
            group=Group.objects.get(name='cust_accnt')
            user.groups.add(group) 
            customer= Customer.objects.create(user=user,)
            customer.save()
            messages.success(request, "Account was created for "+ username)
            return redirect('login')
    context= {'form':form}
    return render(request, 'registration/register.html', context)