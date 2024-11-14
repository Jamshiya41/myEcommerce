from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse

from e_shop.models import Product, Category, SubCategory, Cart, CartItem, ProductVariant, Size, Color


# Create your views here.
def base(request):
    # context ={
    #     "first_name":"Jamshiya",
    #     "second_name":"Adnan"
    # }
    return render(request, 'base.html')
    # return HttpResponse("welcome to my first Django project")


def home(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        categories = Category.objects.all()
        return render(request, 'home.html',
                      {'products': products, 'categories': categories, 'message': 'Welcome, you are logged in!'})
    else:
        products = Product.objects.all()
        categories = Category.objects.all()
        return render(request, 'home.html',
                      {'products': products, 'categories': categories, 'message': 'Hello, Guest! Please log in.'})


def about_details(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        categories = Category.objects.all()
        return render(request, 'about.html',
                      {'products': products, 'categories': categories, 'message': 'Welcome, you are logged in!'})
    else:
        products = Product.objects.all()
        categories = Category.objects.all()
        return render(request, 'about.html',
                      {'products': products, 'categories': categories, 'message': 'Hello, Guest! Please log in.'})


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    categories = Category.objects.all()

    # Retrieve the product variants (size, color, and stock) associated with the product
    variants = ProductVariant.objects.filter(product=product)

    # Get the available sizes and colors from the variants
    available_sizes = variants.values_list('size__id', 'size__name').distinct()
    available_colors = variants.values_list('color__id', 'color__name').distinct()
    print(available_sizes)
    return render(request, 'product_detail.html', {
        'product': product,
        'categories': categories,
        'available_sizes': available_sizes,
        'avail_variant': variants,
        'available_colors': available_colors,
    })


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'product_list.html', {'products': products, 'categories': categories})


def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)  # Get the selected category
    subcategories = SubCategory.objects.filter(category_id=category)  # Filter subcategories by category
    categories = Category.objects.all()
    return render(request, 'category_detail.html',
                  {'category': category, 'categories': categories, 'subcategories': subcategories})


def signup(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        first = request.POST['first']
        last = request.POST['last']
        email = request.POST['email']
        mobile = request.POST['mobile']
        myusers = get_user_model().objects.create_user(username=username, password=password)
        myusers.first_name = first
        myusers.last_name = last
        myusers.email = email
        myusers.save()
        return redirect('signin')
    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)

            # Debugging print statement to ensure we're hitting this point
            print(f"User '{username}' logged in successfully. Redirecting to dashboard.")

            # Redirect to the user dashboard
            return redirect('home')  # Ensure 'user_dash' is the correct URL name
        else:
            # Invalid credentials; show an error message
            # messages.error(request, "Invalid credentials")
            return redirect('signin')

    return render(request, 'signin.html')


def SignOut(request):
    # Log the user out
    logout(request)

    # Redirect to the login page
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html',
                  {'products': products, 'categories': categories, 'message': 'Hello, Guest! Please log in.'})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # size_id = request.POST.get('size')
        # color_id = request.POST.get('color')
        #
        # selected_size = None
        # selected_color = None
        #
        # if size_id:
        #     selected_size = get_object_or_404(Size, id=size_id)
        #
        # if color_id:
        #     selected_color = get_object_or_404(Color, id=color_id)

        # Filter to find the matching variant
        try:
            variant_query = ProductVariant.objects.filter(product_id=product_id)

            # if selected_size:
            #     variant_query = variant_query.filter(size=selected_size)
            #
            # if selected_color:
            #     variant_query = variant_query.filter(color=selected_color)

            variant = variant_query.first()

            if not variant:
                messages.error(request, "This combination of size and color is not available.")
                return redirect('product_detail', product_id=product_id)

        except ProductVariant.MultipleObjectsReturned:
            variant = variant_query.first()

        if variant.quantity <= 0:
            messages.error(request, "This product variant is out of stock.")
            return redirect('product_detail', product_id=product.id)

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if the product variant is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, product_variant=variant)

        # If the item already exists in the cart, increase the quantity
        if not created:
            if cart_item.quantity < variant.quantity:  # Ensure not exceeding stock
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.error(request, "Not enough stock available for this product variant.")
                return redirect('product_detail', product_id=product.id)

        return redirect('cart_detail')

    return redirect('product_detail', product_id=product_id)


def increment_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')  # Redirect back to the cart page


def decrement_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        cart_item.delete()  # Optionally, remove the item if quantity reaches 0
    cart_item.save()
    return redirect('cart_detail')  # Redirect back to the cart page


@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()
    print(items)
    total_price = cart.get_total_price()

    return render(request, 'cart_detail.html', {'cart': cart, 'items': items, 'total_price': total_price})


def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    cart_item.delete()  # Remove the item from the cart

    return JsonResponse({'success': True})


def checkout():
    return None
