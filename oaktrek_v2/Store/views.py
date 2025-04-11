from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib import messages
from django import forms
from django.core.mail import send_mail
from .models import ContactForm

def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def sustainability(request):
    return render(request, 'sustainability.html')

def stores(request):
    return render(request, 'stores.html')

def coming_soon(request):
    return render(request, "coming_soon.html")

def products_view(request, collection_name):
    context = {
        'collection_name': collection_name,
    }
    return render(request, 'products.html', context)

def product_page_view(request, collection_name, product_slug):
    context = {
        'collection_name': collection_name,
        'product_slug': product_slug,
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

