from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib import messages
from django.conf import settings
from django import forms
from django.core.mail import send_mail
from .models import ContactForm

def home(request):
    return render(request, 'index.html', {
        'MEDIA_URL': settings.MEDIA_URL,
    })

def sustainability(request):
    return render(request, 'sustainability.html')

def stores(request):
    return render(request, 'stores.html')

def coming_soon(request):
    return render(request, "coming_soon.html")

def products_view(request, collection_name):
    products = []
    normalized_collection_name = collection_name.lower()
    
    if normalized_collection_name in ["male", "mens", "men's", "men"]:
        collection_name = "Men"
        products = Product.objects.filter(gender="Male")

    if normalized_collection_name in ["Women", "Womens", "Wommen's", "women"]:
        collection_name = "Women"
        products = Product.objects.filter(gender="Female")
    
    context = {
        'products': products,
        'collection_name': collection_name,  
        'original_collection_name': collection_name, 
        "sizes": [8, 9, 10, 11, 12]
    }
    return render(request, 'products.html', context)


def product_page_view(request, collection_name, product_slug):
    if collection_name.lower() in ["male", "mens", "men's", "men"]:
        gender = "Male"
    else:
        gender = None  
    
    product = get_object_or_404(Product, gender=gender, slug=product_slug)
    
    context = {
        'collection_name': collection_name,  
        'product': product,
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