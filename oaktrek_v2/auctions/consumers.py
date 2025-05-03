import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

# In-memory store for auction state (for dev only)
AUCTION_STATE = {}

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.luxury_shoe_id = self.scope['url_route']['kwargs']['luxury_shoe_id']
        self.room_group_name = f'auction_{self.luxury_shoe_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        if self.luxury_shoe_id not in AUCTION_STATE:
            AUCTION_STATE[self.luxury_shoe_id] = {
                'timer': 0,
                'running': False,
                'winner': None
            }

        await self.send(text_data=json.dumps({'timer': AUCTION_STATE[self.luxury_shoe_id]['timer']}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def bid_update(self, event):
        await self.send(text_data=json.dumps({'bid': event['bid']}))
        state = AUCTION_STATE[self.luxury_shoe_id]
        state['timer'] = 10
        if not state['running']:
            state['running'] = True
            asyncio.create_task(self.timer_loop())

    async def timer_update(self, event):
        await self.send(text_data=json.dumps({'timer': event['timer']}))

    async def auction_winner(self, event):
        await self.send(text_data=json.dumps({
            'winner': event['winner'],
            'amount': event['amount']
        }))

    async def timer_loop(self):
        state = AUCTION_STATE[self.luxury_shoe_id]
        while state['timer'] > 0:
            await asyncio.sleep(1)
            state['timer'] -= 1
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'timer_update', 'timer': state['timer']}
            )
        # Timer hit zero, declare winner
        state['running'] = False
        from auctions.models import Bid, LuxuryShoe
        try:
            @database_sync_to_async
            def get_highest_bid():
                return Bid.objects.filter(luxury_shoe_id=self.luxury_shoe_id).order_by('-amount').first()
            @database_sync_to_async
            def get_luxury_shoe():
                return LuxuryShoe.objects.get(id=self.luxury_shoe_id)
            @database_sync_to_async
            def save_luxury_shoe(shoe):
                shoe.is_active = False
                shoe.save()
            highest_bid = await get_highest_bid()
            luxury_shoe = await get_luxury_shoe()
            if luxury_shoe.is_active:
                await save_luxury_shoe(luxury_shoe)
            if highest_bid:
                winner = highest_bid.user.username
                amount = highest_bid.amount
            else:
                winner = None
                amount = None
        except Exception as e:
            winner = None
            amount = None
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'auction_winner', 'winner': winner, 'amount': amount}
        )
