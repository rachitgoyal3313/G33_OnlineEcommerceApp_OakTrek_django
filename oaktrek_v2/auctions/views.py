from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import LuxuryShoe, Bid
from Store.models import Cart

def auction_list(request):
    auctions = LuxuryShoe.objects.filter(is_active=True)
    return render(request, 'auctions/auction_list.html', {'auctions': auctions})

@login_required
def auction_detail(request, luxury_shoe_id):
    luxury_shoe = get_object_or_404(LuxuryShoe, id=luxury_shoe_id)
    highest_bid = Bid.objects.filter(luxury_shoe=luxury_shoe).order_by('-amount').first()
    bid_history = Bid.objects.filter(luxury_shoe=luxury_shoe).order_by('-timestamp')

    # Handle auction ended logic
    if not luxury_shoe.is_active:
        messages.info(request, 'This auction has ended.')
        if highest_bid:
            if highest_bid.user == request.user:
                messages.success(request, f'You won this auction with a bid of ${highest_bid.amount}!')
                # Move product to cart at original price
                add_product_to_cart(request.user, luxury_shoe.product)
                return redirect('checkout')  # Use your checkout URL name
            else:
                messages.info(request, f'This auction was won by {highest_bid.user.username} with a bid of ${highest_bid.amount}.')


    if request.method == 'POST' and luxury_shoe.is_active:
        try:
            bid_amount = float(request.POST.get('amount'))
            if bid_amount <= 0:
                raise ValueError("Bid amount must be positive.")
        except (TypeError, ValueError):
            messages.error(request, 'Please enter a valid bid amount.')
            return render(request, 'auctions/auction_detail.html', {
                'luxury_shoe': luxury_shoe,
                'highest_bid': highest_bid,
                'bid_history': bid_history
            })

        if highest_bid and bid_amount <= highest_bid.amount:
            messages.error(request, f'Your bid must be higher than ${highest_bid.amount}.')
        elif bid_amount < luxury_shoe.starting_bid:
            messages.error(request, f'Your bid must be at least ${luxury_shoe.starting_bid}.')
        else:
            with transaction.atomic():
                new_bid = Bid.objects.create(
                    luxury_shoe=luxury_shoe,
                    user=request.user,
                    amount=bid_amount
                )
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'auction_{luxury_shoe_id}',
                    {
                        'type': 'bid_update',
                        'bid': {
                            'user': request.user.username,
                            'amount': bid_amount,
                            'timestamp': new_bid.timestamp.isoformat()
                        }
                    }
                )
            messages.success(request, 'Your bid has been placed successfully!')
            return redirect('auctions:auction_detail', luxury_shoe_id=luxury_shoe_id)

    return render(request, 'auctions/auction_detail.html', {
        'luxury_shoe': luxury_shoe,
        'highest_bid': highest_bid,
        'bid_history': bid_history
    })

def add_product_to_cart(user, product):
    """
    Adds the product to the user's cart at the product's original price.
    If already present, increments quantity.
    """
    cart_item, created = Cart.objects.get_or_create(
        user=user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
