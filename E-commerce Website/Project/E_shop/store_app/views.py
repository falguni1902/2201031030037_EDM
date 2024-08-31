from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Product, Categories, Filter_Price, Color, Brand, Contact_us
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required
from cart.cart import Cart


def BASE(request):
    return render(request, 'main/base.html')


def Home(request):
    products = Product.objects.filter(status='Publish')

    context = {
        'products': products,
    }

    return render(request, 'main/index.html', context)


def ProductsView(request):
    products = Product.objects.filter(status='Publish')
    categories = Categories.objects.all()
    filter_Price = Filter_Price.objects.all()
    colors = Color.objects.all()
    brands = Brand.objects.all()

    CATEGORIES_TID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get('filter_price')
    COLOR_FILTER_ID = request.GET.get('color_filer')
    BRAND_FILTER_ID = request.GET.get('brand')

    SORT_OPTION = request.GET.get('sort')
    CONDITION_FILTER = request.GET.get('condition')

    if CATEGORIES_TID:
        products = Product.objects.filter(categories=CATEGORIES_TID, status='Publish')
    elif PRICE_FILTER_ID:
        products = Product.objects.filter(filter_price=PRICE_FILTER_ID, status='Publish')
    elif COLOR_FILTER_ID:
        products = Product.objects.filter(filter_price=COLOR_FILTER_ID, status='Publish')
    elif BRAND_FILTER_ID:
        products = Product.objects.filter(brand=BRAND_FILTER_ID, status='Publish')
    elif SORT_OPTION:
        products = products.order_by(SORT_OPTION)
    elif CONDITION_FILTER == 'New':
        products = products.filter(status='publish', condition='New')
    elif CONDITION_FILTER == 'Old':
        products = products.filter(status='publish', condition='Old')
    else:
        products = Product.objects.all()
        # products = Product.objects.filter(status='publish')

    context = {
        'products': products,
        'categories': categories,
        'filter_Price': filter_Price,
        'colors': colors,
        'brands': brands
    }

    return render(request, 'main/products.html', context)


def SearchView(request):
    query = request.GET.get('Query')
    products = Product.objects.filter(name__icontains=query)

    context = {
        'products': products
    }

    return render(request, 'main/search.html', context)


def ProductDetailsPageView(request, id):
    product = Product.objects.filter(id=id).first()

    context = {
        'product': product
    }

    return render(request, 'main/single_product.html', context)


def Contact_pageView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message, )

        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        try:
            send_mail(subject, message, email_from, ['maulikpatoliya21@gmail.com'])
            contact.save()
            messages.success(request, 'Your message was sent successfully!')
            # return redirect('home')
        except:
            messages.error(request, 'There was an error sending your message. Please try again.')
            return redirect('contact')

    return render(request, 'main/contact.html')


def RegistrationView(request):
    if request.method == 'POST':
        if request.method == 'POST':
            uname = request.POST.get('username')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            password1 = request.POST.get('pass1')
            password2 = request.POST.get('pass2')

            if password1 == password2:
                try:
                    Customer = User.objects.create_user(uname, email, password1)
                    Customer.firstname = firstname
                    Customer.lastname = lastname
                    Customer.save()
                    messages.success(request,
                                     'Your Registration has been successfully completed!!. You can now log in.')
                    return redirect('registration')
                except Exception as e:
                    messages.error(request, f'Error creating account: {e}')
            else:
                messages.error(request, 'Passwords do not match.')

    return render(request, 'registration/authentication.html')


def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect")
            # return HttpResponse("Username or Password is incorrect")

    return render(request, 'registration/authentication.html')


def LogoutView(request):
    logout(request)
    return redirect('home')


# def ResetPasswordView(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         user = User.objects.filter(email=email).first()
#
#         if user:
#             messages.success(request,
#                              "The link to reset the password has been sent to your email. Please check your email.")
#             return redirect('password_reset')
#         else:
#             messages.success(request, "Invalid Email, User not found with this email id.")
#     return render(request, 'forgot_password.html')
#
#
# def ResetConfirmView(request, uidb64, token):
#     return PasswordResetConfirmView.as_view(
#         template_name='reset_password.html',
#         success_url=reverse_lazy('login')
#     )(request, uidb64=uidb64, token=token)


@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'cart/cart_details.html')


def Checkout(request):
    return render(request, 'cart/check_out.html')
