from django.db import models
from django.utils import timezone

class ChatHistory(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        app_label = 'chat_app'  # Add this line explicitly
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"User: {self.user_message[:50]}... | Bot: {self.bot_response[:50]}..."