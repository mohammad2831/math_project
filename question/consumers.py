from channels.generic.websocket import AsyncWebsocketConsumer
import json



class ScoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f"user_{self.user_id}"
        print(f"user_{self.user_id}")

        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'WebSocket connection established',
            'user_id': self.user_id
        }))











    async def receive(self, text_data):
        if not text_data:
            await self.send(text_data=json.dumps({'error': 'Empty message received'}))
            return

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
           
            await self.send(text_data=json.dumps({'error': 'Invalid JSON format'}))
            return

        message = data.get('message')
        await self.send(text_data=json.dumps({
            'message': f"Received: {message}"
        }))

    
    
    
    
    async def send_score(self, event):
        print("test ws")
        await self.send(text_data=json.dumps({
            'score': event['score'],
            'mistake': event['mistake']}))












        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        from question.models import YourUserModel
        user = await YourUserModel.objects.aget(id=self.user_id)
        user.is_online = False
        await user.asave()

        print(f"User {self.user_id} disconnected. Close code: {close_code}")