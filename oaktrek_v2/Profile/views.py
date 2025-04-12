from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Address
from django.db import IntegrityError
from Store.models import Order
from django.contrib.auth.models import User  # Using Django's built-in User model
from django.contrib.auth.decorators import login_required




# from django.shortcuts import render, redirect
# from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required




def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        cpassword = request.POST.get('password2')

        if password != cpassword:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=name).exists():  # Check if username exists
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():  # Check if email exists
            messages.error(request, 'Email already exists')
        else:
            # Create user with name as username
            user = User.objects.create_user(
                username=name,  # Use name as username
                email=email,
                password=password
            )
            # Instead of logging in automatically, just show a success message
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('auth')  # Or redirect to 'login' if you have a separate login page
    return render(request, 'auth.html')



def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Email and password are required')
            return redirect('login')
        
        # Find user by email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged out successfully!')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    
    # If not POST, show the auth page
    return render(request, 'auth.html')

def auth_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'auth.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')


@login_required
def admin_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Email and password are required')
            return redirect('admin_login')
        
        # Find user by email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                # Check if user is a superuser
                if user.is_superuser:
                    login(request, user)
                    messages.success(request, 'Admin login successful!')
                    return redirect('admin:index')  # Redirect to Django admin dashboard
                else:
                    messages.error(request, 'You do not have admin privileges')
                    return redirect('admin_login')
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('admin_login')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('admin_login')
    
    # If not POST, show the admin login page
    return render(request, 'admin_login.html')

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user)
    addresses = Address.objects.filter(user=request.user)
    
    # Check if user is staff or admin
    is_admin = request.user.is_staff or request.user.is_superuser
    
    return render(request, 'profile.html', {
        'user': request.user, 
        'orders': orders,
        'addresses': addresses,
        'is_admin': is_admin  # Pass this to template
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('change_password')

    form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required
def add_address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        is_default = 'is_default' in request.POST

        if not all([name, street, city, state, zipcode]):
            messages.error(request, 'All address fields are required')
            return redirect('profile')

        try:
            if is_default:
                Address.objects.filter(user=request.user, is_default=True).update(is_default=False)

            address = Address(
                name=name, street=street, city=city, state=state, 
                zipcode=zipcode, is_default=is_default, user=request.user
            )
            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('profile')
        except IntegrityError as e:
            messages.error(request, f'Error adding address: {str(e)}')
            return redirect('profile')


@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)

    if address.user != request.user:
        messages.error(request, 'You do not have permission to delete this address.')
        return redirect('profile')

    try:
        address.delete()
        messages.success(request, 'Address deleted successfully!')
        return redirect('profile')
    except Exception as e:
        messages.error(request, f'Error deleting address: {str(e)}')
        return redirect('profile')


@login_required
def add_phone(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if not phone:
            messages.error(request, 'Phone number is required')
            return redirect('profile')

        try:
            # If you have a profile model with phone field
            profile = request.user.profile
            profile.phone = phone
            profile.save()
            messages.success(request, 'Phone number added successfully!')
            return redirect('profile')
        except AttributeError:
            # If you don't have a profile model, you can add custom logic here
            messages.error(request, 'Profile model not found')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'Error adding phone number: {str(e)}')
            return redirect('profile')
        
        



@login_required
def admin_signin(request):
    if request.method == 'POST':
        email = request.POST.get('admin_email')
        password = request.POST.get('admin_password')
        
        if not email or not password:
            messages.error(request, 'Email and password are required')
            return redirect('profile')
        
        try:
            user = User.objects.get(email=email)
            authenticated_user = authenticate(request, username=user.username, password=password)
            
            if authenticated_user and authenticated_user.is_staff:
                login(request, authenticated_user)
                messages.success(request, 'Admin sign-in successful!')
                
                # Optional: store admin status in session
                request.session['is_admin'] = True
                
                return redirect('adminProducts.html')
            else:
                messages.error(request, 'Invalid credentials or insufficient permissions')
                return redirect('profile')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('profile')
    
    # If GET request, redirect to profile
    return redirect('profile')



@login_required
def address_list_view(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'addresses.html', {'addresses': addresses})
