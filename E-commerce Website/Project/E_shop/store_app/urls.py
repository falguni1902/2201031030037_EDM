from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.Home, name='home'),
                  path('base/', views.BASE, name='base'),
                  path('products/', views.ProductsView, name='products'),
                  path('product_details/<str:id>', views.ProductDetailsPageView, name='product_details'),
                  path('contact/', views.Contact_pageView, name='contact'),

                  path('search/', views.SearchView, name='search'),

                  path('registration/', views.RegistrationView, name='registration'),
                  path('login/', views.LoginView, name='login'),
                  path('logout/', views.LogoutView, name='logout'),
                  # path('password_reset/', views.ResetPasswordView, name='password_reset'),
                  # path('password-reset-confirm/<uidb64>/<token>/', views.ResetConfirmView, name='password_reset_confirm'),

                  # Cart
                  path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
                  path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
                  path('cart/item_increment/<int:id>/',
                       views.item_increment, name='item_increment'),
                  path('cart/item_decrement/<int:id>/',
                       views.item_decrement, name='item_decrement'),
                  path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
                  path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
                  path('cart/checkout/', views.Checkout, name='checkout'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
