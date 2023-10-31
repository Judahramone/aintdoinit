from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductListView.as_view(), name= 'products'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:product_id>/create_mod/', views.createMod, name='create_mod'),
    path('product/<int:product_id>/delete_mod/<int:mod_id>', views.deleteMod, name='delete_mod'),
    path('product/<int:product_id>/update_mod/<int:mod_id>', views.updateMod, name='update_mod'),
    path('product/update_product/<int:product_id>/', views.updateProduct, name='update_product'),
    path('product/create_product/', views.createProduct, name='create_product'),  # Point to createProduct view
    path('product/delete_product/<int:product_id>/', views.deleteProduct, name='delete_product'),  # Point to deleteProduct view and added product_id param
    path('toggle_dark_mode/', views.toggle_dark_mode, name='toggle_dark_mode'),
]