from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductListView.as_view(), name= 'products'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:product_id>/create_variation/', views.createVariation, name='create_variation'),
    path('product/<int:product_id>/delete_variation/<int:variation_id>', views.deleteVariation, name='delete_variation'),
    path('product/<int:product_id>/update_variation/<int:variation_id>', views.updateVariation, name='update_variation'),
    path('product/update_product/<int:product_id>/', views.updateProduct, name='update_product'),
    path('product/create_product/', views.createProduct, name='create_product'),  # Point to createProduct view
    path('product/delete_product/<int:product_id>/', views.deleteProduct, name='delete_product'),  # Point to deleteProduct view and added product_id param
    path('toggle_dark_mode/', views.toggle_dark_mode, name='toggle_dark_mode'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)