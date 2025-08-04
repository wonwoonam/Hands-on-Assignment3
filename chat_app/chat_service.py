from .models import ChatHistory
from .bot_manager import BotManager

class ChatService:
    def __init__(self):
        self.bot_manager = BotManager()
    
    def process_message(self, user_message):
        """Process user message and return bot response"""
        # Get bot response
        bot_response = self.bot_manager.get_response(user_message)
        
        # Save to database
        ChatHistory.objects.create(
            user_message=user_message,
            bot_response=bot_response
        )
        
        return bot_response
    
    def get_chat_history(self, limit=10):
        """Retrieve recent chat history"""
        return ChatHistory.objects.all()[:limit]