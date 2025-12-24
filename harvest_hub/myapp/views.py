from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Profile, Product
from .forms import ProductForm


# --------------------------------------------------
# HOME
# --------------------------------------------------
def home_view(request):
    return render(request, 'myapp/home.html')


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect('home')


# --------------------------------------------------
# LOGIN
# --------------------------------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('home')

    return redirect('home')


# --------------------------------------------------
# REGISTRATION (FIXED)
# --------------------------------------------------
def register_view(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        username = request.POST.get("username")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        address = request.POST.get("address")
        category = request.POST.get("category")

        # Validate password match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('home')

        # Check unique username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('home')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=name
        )

        # Create profile (NO SIGNALS)
        Profile.objects.create(
            user=user,
            mobile=mobile,
            address=address,
            category=category
        )

        # Login user
        login(request, user)
        messages.success(request, "Registration successful.")
        return redirect('home')

    return redirect('home')


# --------------------------------------------------
# CART VIEW
# --------------------------------------------------
@login_required
def cart_view(request):
    cart = request.session.get('cart', {})

    if isinstance(cart, list):
        cart = {str(pid): 1 for pid in cart}
        request.session['cart'] = cart

    products = Product.objects.filter(id__in=cart.keys())

    cart_products = []
    total_price = 0

    for product in products:
        qty = cart.get(str(product.id), 0)
        total = product.price * qty
        total_price += total

        product.quantity = qty
        product.total_price = total
        cart_products.append(product)

    return render(request, 'myapp/cart.html', {
        'cart_products': cart_products,
        'total_price': total_price
    })


# --------------------------------------------------
# ADD TO CART
# --------------------------------------------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if isinstance(cart, list):
        cart = {str(pid): 1 for pid in cart}

    qty = 1
    if request.method == 'POST':
        try:
            qty = int(request.POST.get("quantity", 1))
            if qty < 1:
                qty = 1
        except:
            qty = 1

    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + qty

    request.session['cart'] = cart
    messages.success(request, f"{product.name} added to cart.")
    return redirect('digital_market')


# --------------------------------------------------
# UPDATE CART
# --------------------------------------------------
@login_required
def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)
    action = request.GET.get('action')

    if pid not in cart:
        if action == 'add':
            cart[pid] = 1
    else:
        if action == 'add':
            cart[pid] += 1
        elif action == 'subtract':
            cart[pid] -= 1
            if cart[pid] < 1:
                del cart[pid]

    request.session['cart'] = cart
    return redirect('cart')


# --------------------------------------------------
# REMOVE FROM CART
# --------------------------------------------------
@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        del cart[pid]
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Item not found.")

    request.session['cart'] = cart
    return redirect('cart')


# --------------------------------------------------
# OTHER STATIC PAGES
# --------------------------------------------------
def inventory_view(request):
    return render(request, 'myapp/inventory.html')


def sales_view(request):
    return render(request, 'myapp/sales.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        print(f"Contact message from {name} ({email}): {message}")

        messages.success(request, "Your message has been sent!")
        return redirect('contact')

    return render(request, 'myapp/contact.html')


# --------------------------------------------------
# PROFILE
# --------------------------------------------------
@login_required
def profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user.first_name = request.POST.get("first_name", user.first_name)
        user.email = request.POST.get("email", user.email)
        user.save()

        profile.mobile = request.POST.get("mobile", profile.mobile)
        profile.address = request.POST.get("address", profile.address)
        profile.category = request.POST.get("category", profile.category)

        if 'image' in request.FILES:
            profile.image = request.FILES['image']

        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render(request, 'myapp/profile.html', {
        'user': user,
        'profile': profile
    })


# --------------------------------------------------
# PRODUCT UPLOAD
# --------------------------------------------------
@login_required
def upload_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            messages.success(request, "Product uploaded successfully.")
            return redirect('profile')
    else:
        form = ProductForm()

    return render(request, 'myapp/upload_product.html', {'form': form})


# --------------------------------------------------
# DELETE PRODUCT
# --------------------------------------------------
@login_required
def delete_product_view(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, user=request.user)
        product.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


# --------------------------------------------------
# MARKET VIEW
# --------------------------------------------------
def market_view(request):
    products = Product.objects.all()
    return render(request, 'myapp/market.html', {'products': products})


# --------------------------------------------------
# CHECKOUT
# --------------------------------------------------
def checkout(request):
    if request.method == 'POST':
        if 'cart' in request.session:
            del request.session['cart']

        request.session.modified = True
        return render(request, 'myapp/checkout.html')

    return redirect('cart')
