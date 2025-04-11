from django.contrib.auth import login, authenticate,logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import Address
from django.db import IntegrityError
from Store.models import Order
from .models import User
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not all([username, email, password1, password2]):
            return JsonResponse({'message': 'All fields are required'}, status=400)

        if password1 != password2:
            return JsonResponse({'message': 'Passwords do not match'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already taken'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email already registered'}, status=400)

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return JsonResponse({'message': 'Account created successfully!', 'redirect': reverse('profile')})
        except Exception as e:
            return JsonResponse({'message': f'Error creating account: {str(e)}'}, status=500)

    return render(request, 'auth.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({'redirect': reverse('profile'), 'message': 'Logged in successfully!'})
        else:
            return JsonResponse({'message': 'Invalid email or password'}, status=401)

    form = AuthenticationForm()
    return render(request, 'auth.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def profile_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'profile.html', {'user': request.user, 'orders': orders})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return JsonResponse({'message': 'Password changed successfully!'})
        else:
            return JsonResponse({'message': 'Error changing password'}, status=400)

    form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def add_address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        is_default = 'is_default' in request.POST

        if not all([name, street, city, state, zipcode]):
            return JsonResponse({'message': 'All address fields are required'}, status=400)

        try:
            if is_default:
                Address.objects.filter(user=request.user, is_default=True).update(is_default=False)

            address = Address(
                name=name, street=street, city=city, state=state, 
                zipcode=zipcode, is_default=is_default, user=request.user
            )
            address.save()
            return JsonResponse({'message': 'Address added successfully!'})
        except IntegrityError as e:
            return JsonResponse({'message': f'Error adding address: {str(e)}'}, status=400)

def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)

    if address.user != request.user:
        return JsonResponse({'message': 'You do not have permission to delete this address.'}, status=403)

    try:
        address.delete()
        return JsonResponse({'message': 'Address deleted successfully!'})
    except Exception as e:
        return JsonResponse({'message': f'Error deleting address: {str(e)}'}, status=400)

def add_phone(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if not phone:
            return JsonResponse({'message': 'Phone number is required'}, status=400)

        try:
            request.user.profile.phone = phone  # Assuming you have a profile model that stores phone
            request.user.profile.save()
            return JsonResponse({'message': 'Phone number added successfully!'})
        except Exception as e:
            return JsonResponse({'message': f'Error adding phone number: {str(e)}'}, status=400)
        
@login_required
def address_list_view(request):
    addresses = Address.objects.filter(user=request.user).values(
        'id', 'name', 'street', 'city', 'state', 'zipcode', 'is_default'
    )
    return JsonResponse({'addresses': list(addresses)})

