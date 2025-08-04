from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import os

class BotManager:
    def __init__(self):
        self.chatbot = ChatBot(
            'TerminalBot',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri='sqlite:///chatbot_database.sqlite3',
            logic_adapters=[
                'chatterbot.logic.BestMatch',
                'chatterbot.logic.MathematicalEvaluation',
                'chatterbot.logic.TimeLogicAdapter',
            ]
        )
        self.is_trained = False
    
    def train_bot(self):
        """Train the bot with corpus data and custom conversations"""
        if not self.is_trained:
            print("Training the bot... This may take a moment.")
            
            # Train with English corpus
            corpus_trainer = ChatterBotCorpusTrainer(self.chatbot)
            corpus_trainer.train('chatterbot.corpus.english.greetings')
            corpus_trainer.train('chatterbot.corpus.english.conversations')
            
            # Train with custom conversations
            list_trainer = ListTrainer(self.chatbot)
            
            # Add some custom training data
            custom_conversations = [
                "Good morning! How are you doing?",
                "I am doing very well, thank you for asking.",
                "You're welcome.",
                "Do you like hats?",
                "What is your name?",
                "I am a ChatBot created to help you.",
                "How can I help you today?",
                "I'm here to chat and answer your questions.",
                "What do you like to do for fun?",
                "I enjoy having conversations and learning new things.",
                "Tell me about yourself",
                "I am an AI chatbot designed to have conversations with humans.",
                "What's the weather like?",
                "I don't have access to current weather data, but I'd love to chat about other topics!",
                "Goodbye",
                "Goodbye! It was nice chatting with you.",
                "Thank you",
                "You're very welcome!",
            ]
            
            list_trainer.train(custom_conversations)
            self.is_trained = True
            print("Bot training completed!")
    
    def get_response(self, user_input):
        """Get bot response for user input"""
        if not self.is_trained:
            self.train_bot()
        
        response = self.chatbot.get_response(user_input)
        return str(response)
