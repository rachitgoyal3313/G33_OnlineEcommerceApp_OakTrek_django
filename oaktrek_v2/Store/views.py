from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Order, OrderItem
from Profile.models import Address
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings
from django import forms
from django.core.mail import send_mail
from .models import ContactForm
from django.db.models import Q
import re
import uuid

def home(request):
    return render(request, 'index.html', {
        'MEDIA_URL': settings.MEDIA_URL,
    })

def normalize_gender_query(query):
    query = query.lower()

    male_keywords = ['men', "men's", 'mens', 'man', 'male', 'boys', 'dudes', 'queer','rachit', 'divyansh', 'pushkar', 'handsome']
    female_keywords = ['women', "women's", 'womens', 'lady', 'ladies', 'female', 'girls', 'gay', 'bi', 'queer', 'abhinav', 'sexy' ]
    unisex_keywords = ['unisex', 'all', 'any', 'everyone', 'nonbinary', 'pan', 'fab', 'slay']

    for word in male_keywords:
        if re.search(rf'\b{re.escape(word)}\b', query):
            return 'Male'
    for word in female_keywords:
        if re.search(rf'\b{re.escape(word)}\b', query):
            return 'Female'
    for word in unisex_keywords:
        if re.search(rf'\b{re.escape(word)}\b', query):
            return 'Unisex'

    return None

def search(request):
    """
    Search view that handles product search functionality
    """
    query = None
    results = None

    if 'q' in request.GET:
        query = request.GET.get('q').strip()
        if query:
            normalized_gender = normalize_gender_query(query)

            # Build search filter
            filters = (
                Q(category__icontains=query) |
                Q(product_name__icontains=query)
            )

            if normalized_gender:
                filters |= Q(gender__iexact=normalized_gender)
            else:
                filters |= Q(gender__icontains=query)

            results = Product.objects.filter(filters)

    products_with_images = []
    if results:
        for product in results:
            product_images = [img for img in [
                product.image_1, product.image_2,
                product.image_3, product.image_4, product.image_5
            ] if img]

            products_with_images.append({
                'product': product,
                'images': product_images
            })

    context = {
        'query': query,
        'results': results,
        'products_with_images': products_with_images,
        'is_search_results': True,
    }

    return render(request, 'search_results.html', context)


def sustainability(request):
    return render(request, 'sustainability.html')

def stores(request):
    return render(request, 'stores.html')

def coming_soon(request):
    return render(request, "coming_soon.html")

def products_cat_view(request, gender, collection_name):
    products = []
    normalized_gender = gender.lower()
    category = None
    gender = None
    if normalized_gender in ["male", "mens", "men's", "men"]:
        gender = "Male"
        # products = Product.objects.filter(gender="Male")
        # category = "Men"

    elif normalized_gender in ["Women", "Womens", "Wommen's", "women"]:
        gender = "Female"
        category = "Women"
        # products = Product.objects.filter(gender="Female")


    products = Product.objects.filter(gender=gender, category_slug = collection_name)

    category = products[1].category
    
    context = {
        'products': products,
        'collection_name': collection_name,  
        'original_collection_name': collection_name,  
        'product_category': category, 
        "sizes": [8, 9, 10, 11, 12]
    }


    return render(request, 'products.html', context)




def products_view(request, collection_name):
    products = []
    normalized_collection_name = collection_name.lower()
    category = None
    if normalized_collection_name in ["male", "mens", "men's", "men"]:
        collection_name = "Men"
        products = Product.objects.filter(gender="Male")
        category = "Men"

    elif normalized_collection_name in ["Women", "Womens", "Wommen's", "women"]:
        collection_name = "Women"
        category = "Women"
        products = Product.objects.filter(gender="Female")
    
    else:
         products = Product.objects.filter(category_slug=collection_name)
         category = products[1].category

    sort_by = request.GET.get('sort', 'featured')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'relevance':
        # For random ordering in Django
        products = products.order_by('?')
    
    context = {
        'products': products,
        'collection_name': collection_name,  
        'original_collection_name': collection_name,  
        'product_category': category, 
        "sizes": [8, 9, 10, 11, 12]
    }
    return render(request, 'products.html', context)


def product_page_view(request, collection_name, product_slug):
    product = None
    if collection_name.lower() in ["male", "mens", "men's", "men"]:
        gender = "Male"
        product = get_object_or_404(Product, gender=gender, slug=product_slug)
    elif collection_name.lower() in ["Women", "Womens", "Wommen's", "women"]:
        gender = "Female"
        product = get_object_or_404(Product, gender=gender, slug=product_slug)
    else:
        product = get_object_or_404(Product, category_slug=collection_name, slug=product_slug)

    product_images = []
    for img in [product.image_1, product.image_2, product.image_3, product.image_4, product.image_5]:
        if img:
            product_images.append(img)


    # Normalize collection_name to match the gender field
    
    # Query the product by slug and gender
    
    context = {
        "sizes": [8, 9, 10, 11, 12],
        'collection_name': collection_name,  # For URL consistency
        'product': product,
        'product_images': product_images,
    }

    return render(request, 'product_page.html', context)


def moonshot(request):
    return render(request, 'moonshot.html')

def mothernature(request):
    return render(request, 'moonshot.html')

def adidasxoaktrek(request):
    return render(request, 'adidasxoaktrek.html')

def bcorp(request):
    return render(request, 'bcorp.html')

def carbonFootprint(request):
    return render(request, 'carbonoffsets.html')

def oaktrek_help(request):
    context = {
        'form_submitted': False
    }
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject'] or 'Contact Form Submission'
        message = form.cleaned_data['message']
        try:
            send_mail(
                subject=subject,
                message=f"From: {name}\nEmail: {email}\n\n{message}",
                from_email=email,
                recipient_list=['your-email@example.com'],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('oaktrek_help')
        except Exception:
            messages.error(request, 'There was an error sending your message.')
        context['form_submitted'] = True
    return render(request, 'oaktrek_help.html', {'form': form})


def faq(request):
    return render(request, 'faq.html')

def returns(request):
    return render(request, 'returns.html')

def aboutUs(request):
    return render(request, 'about_us.html')

def our_story(request):
    return render(request, 'our_story.html')

def our_materials(request):
    return render(request, 'our_materials.html')

def sustainability(request):
    return render(request, 'sustainability.html')

def regenerative(request):
    return render(request, 'regenerative.html')

def renewable(request):
    return render(request, 'renewable.html')

def terms(request):
    return render(request, 'terms.html')

def responsibleEnergy(request):
    return render(request, 'responsibleenergy.html')

@login_required
def cart_view(request):
    user = request.user

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')

        product = get_object_or_404(Product, id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)

        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

        return redirect('cart')

    # GET request
    cart_items = Cart.objects.filter(user=user).select_related('product')
    total = sum(item.product.price * item.quantity for item in cart_items)
    tax = total * 0.28
    context = {
        'cart_items': cart_items,
        'tax' : tax,
        'subtotal' : total,
        'total': total + tax,
    }
    return render(request, 'cart.html', context)


@login_required
@transaction.atomic
def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user).select_related('product')
    
    if not cart_items.exists():
        return redirect('cart')  # Redirect to cart if it's empty

    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        
        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            return render(request, 'checkout.html', {
                'error': 'Invalid address selected.',
                'cart_items': cart_items,
                'total_amount': total_amount,
                'addresses': user.addresses.all()
            })

        # Create the order
        order = Order.objects.create(
            user=user,
            address=address,
            total_amount=total_amount
        )

        # Create order items (you might want to create an OrderItem model)
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Clear the user's cart
        cart_items.delete()

        return redirect('order_confirmation', order_id=order.id)
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    tax = total * 0.28
    context = {
        'cart_items': cart_items,
        'tax' : tax,
        'subtotal' : total,
        'total': total + tax,
        'addresses': user.addresses.all(),
    }

    return render(request, 'checkout.html', context)


@login_required
def order_confirmation(request, order_id):
    """
    View function to display the order confirmation page after a successful checkout.
    
    Args:
        request: The HTTP request object
        order_id: The ID of the order to display confirmation for
    
    Returns:
        Rendered confirmation.html template with order details
    """
    # Get the order or return 404 if not found
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Get all order items related to this order
    order_items = order.items.all().select_related('product')
    
    address = Address.objects.all().filter(user=request.user)

    # Calculate order totals
    subtotal = sum(item.price * item.quantity for item in order_items)
    tax = subtotal * 0.28  # Same tax calculation as in checkout
    total = subtotal + tax
    
    # Generate a formatted order number (you could also use the order ID directly)
    order_number = f"OAK-{order.id}-{uuid.uuid4().hex[:6].upper()}"
    
    # Prepare order items for the template with the required format
    formatted_items = []
    for item in order_items:
        formatted_items.append({
            'name': item.product.product_name,
            'quantity': item.quantity,
            'price': item.price,
            'image': item.product.image_1.url,
            # If you have product images, you could include them here
            # 'image': item.product.image_1.url if item.product.image_1 else '',
        })
    
    # Prepare the context for the template
    context = {
        'order_number': order_number,
        'order_items': formatted_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
        'user': request.user,
        'addresses': address
    }
    
    return render(request, 'confirmation.html', context)