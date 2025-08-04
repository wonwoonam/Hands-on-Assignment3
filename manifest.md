# Django ChatterBot Terminal Client - Complete Project Manifest

## Project Overview

A terminal-based chat client built with Django that allows users to have conversations with an AI bot through the command line interface. The project includes both ChatterBot integration and a mock bot fallback for compatibility issues.

## Features

- 🤖 Interactive terminal chat interface
- 💾 Persistent conversation history storage
- 🧠 Machine learning-based responses (or mock responses)
- ⚡ Special commands (history, clear, help, quit)
- 🔧 Django admin interface for chat history management
- 🛡️ Error handling and graceful exits
- 📱 Mock bot fallback for compatibility issues

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (for both Django and ChatterBot)
- **AI Engine**: ChatterBot 1.0.8+ (with mock fallback)
- **Python**: 3.7-3.9 (recommended for ChatterBot compatibility)

## Project Structure

```
chat_project/
├── manage.py                           # Django management script
├── requirements.txt                    # Project dependencies
├── run_chat.py                        # Direct chat runner script
├── README.md                          # Project documentation
├── .gitignore                         # Git ignore file
├── db.sqlite3                         # Django database (generated)
├── chatbot_database.sqlite3           # ChatterBot database (generated)
│
├── chat_project/                      # Django project configuration
│   ├── __init__.py
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # URL routing
│   ├── wsgi.py                        # WSGI configuration
│   └── asgi.py                        # ASGI configuration
│
└── chat_app/                          # Main Django application
    ├── __init__.py
    ├── admin.py                       # Django admin configuration
    ├── apps.py                        # App configuration
    ├── models.py                      # Database models
    ├── views.py                       # Django views (unused)
    ├── tests.py                       # Unit tests
    ├── bot_manager.py                 # Bot management and training
    ├── chat_service.py                # Business logic layer
    ├── terminal_client.py             # Terminal interface
    │
    ├── migrations/                    # Database migrations
    │   ├── __init__.py
    │   └── 0001_initial.py           # Generated migration
    │
    └── management/                    # Django management commands
        ├── __init__.py
        └── commands/
            ├── __init__.py
            └── start_chat.py          # Custom Django command
```

## Installation Guide

### 1. Prerequisites

- Python 3.7-3.9 (recommended for ChatterBot compatibility)
- pip package manager

### 2. Create Project Structure

```bash
# Create Django project
django-admin startproject chat_project
cd chat_project

# Create Django app
python manage.py startapp chat_app

# Create management command structure
mkdir -p chat_app/management/commands
touch chat_app/management/__init__.py
touch chat_app/management/commands/__init__.py
```

### 3. Install Dependencies

Create `requirements.txt`:
```txt
Django>=4.2.0
chatterbot>=1.0.8
chatterbot-corpus>=1.2.0
```

Install packages:
```bash
# Try ChatterBot first
pip install -r requirements.txt

# If ChatterBot fails (common on Apple Silicon), just install Django
pip install Django
```

### 4. Configure Django Settings

Update `chat_project/settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chat_app',  # Add this line
]
```

### 5. Create Database Tables

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

## File Contents

### Core Django Files

#### `chat_project/settings.py`
```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chat_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chat_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

#### `chat_project/urls.py`
```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

### Chat Application Files

#### `chat_app/apps.py`
```python
from django.apps import AppConfig

class ChatAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat_app'
```

#### `chat_app/models.py`
```python
from django.db import models
from django.utils import timezone

class ChatHistory(models.Model):
    user_message = models.TextField(help_text="Message sent by the user")
    bot_response = models.TextField(help_text="Response generated by the bot")
    timestamp = models.DateTimeField(default=timezone.now, help_text="When the conversation occurred")
    
    class Meta:
        app_label = 'chat_app'
        ordering = ['-timestamp']
        verbose_name = "Chat History"
        verbose_name_plural = "Chat Histories"
    
    def __str__(self):
        return f"User: {self.user_message[:30]}... | Bot: {self.bot_response[:30]}..."
```

#### `chat_app/admin.py`
```python
from django.contrib import admin
from .models import ChatHistory

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['user_message_preview', 'bot_response_preview', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['user_message', 'bot_response']
    readonly_fields = ['timestamp']
    
    def user_message_preview(self, obj):
        return obj.user_message[:50] + "..." if len(obj.user_message) > 50 else obj.user_message
    user_message_preview.short_description = 'User Message'
    
    def bot_response_preview(self, obj):
        return obj.bot_response[:50] + "..." if len(obj.bot_response) > 50 else obj.bot_response
    bot_response_preview.short_description = 'Bot Response'
```

#### `chat_app/bot_manager.py`
```python
import random
import re

class MockChatBot:
    """Simple mock chatbot for testing when ChatterBot isn't available"""
    
    def __init__(self, name):
        self.name = name
        self.responses = {
            'greeting': [
                "Hello! How are you doing?",
                "Hi there! Nice to meet you!",
                "Good day! How can I help you?",
                "Hello! What's on your mind today?"
            ],
            'how_are_you': [
                "I am doing very well, thank you for asking.",
                "I'm great! Thanks for asking. How about you?",
                "I'm doing wonderful, thanks!",
                "Pretty good! Thanks for asking."
            ],
            'thanks': [
                "You're welcome!",
                "My pleasure!",
                "Glad I could help!",
                "Anytime!"
            ],
            'goodbye': [
                "Goodbye! It was nice chatting with you.",
                "See you later! Have a great day!",
                "Bye! Thanks for the conversation!",
                "Take care! Come back anytime!"
            ],
            'question': [
                "Do you like hats?",
                "What's your favorite color?",
                "Do you enjoy reading books?",
                "What do you like to do for fun?",
                "Have you seen any good movies lately?"
            ],
            'default': [
                "That's interesting! Tell me more.",
                "I see. What else would you like to talk about?",
                "Hmm, that's a good point.",
                "I understand. Anything else on your mind?",
                "That makes sense. What do you think about it?",
                "Interesting perspective! What else?",
                "I hear you. Tell me more about that.",
                "That's cool! What's your take on it?"
            ]
        }
    
    def get_response(self, user_input):
        """Generate a response based on simple pattern matching"""
        user_input = user_input.lower().strip()
        
        # Greeting patterns
        if any(word in user_input for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return random.choice(self.responses['greeting'])
        
        # How are you patterns
        if any(phrase in user_input for phrase in ['how are you', 'how do you do', 'how are things']):
            return random.choice(self.responses['how_are_you'])
        
        # Thank you patterns
        if any(word in user_input for word in ['thank', 'thanks', 'appreciate']):
            return random.choice(self.responses['thanks'])
        
        # Goodbye patterns
        if any(word in user_input for word in ['bye', 'goodbye', 'see you', 'farewell', 'take care']):
            return random.choice(self.responses['goodbye'])
        
        # Welcome response
        if "you're welcome" in user_input or "welcome" in user_input:
            return random.choice(self.responses['question'])
        
        # Default response
        return random.choice(self.responses['default'])

class BotManager:
    def __init__(self):
        self.chatbot = MockChatBot('TerminalBot')
        self.is_trained = False
    
    def train_bot(self):
        """Mock training - just set the flag"""
        if not self.is_trained:
            print("Training the mock bot... Done!")
            self.is_trained = True
            print("Bot ready! This is a simple mock bot that simulates ChatterBot functionality.")
    
    def get_response(self, user_input):
        """Get bot response for user input"""
        if not self.is_trained:
            self.train_bot()
        
        response = self.chatbot.get_response(user_input)
        return str(response)

# Alternative ChatterBot implementation (use if ChatterBot installs successfully)
"""
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

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
        if not self.is_trained:
            print("Training the bot... This may take a moment.")
            
            corpus_trainer = ChatterBotCorpusTrainer(self.chatbot)
            corpus_trainer.train('chatterbot.corpus.english.greetings')
            corpus_trainer.train('chatterbot.corpus.english.conversations')
            
            list_trainer = ListTrainer(self.chatbot)
            custom_conversations = [
                "Good morning! How are you doing?",
                "I am doing very well, thank you for asking.",
                "You're welcome.",
                "Do you like hats?",
            ]
            list_trainer.train(custom_conversations)
            self.is_trained = True
            print("Bot training completed!")
    
    def get_response(self, user_input):
        if not self.is_trained:
            self.train_bot()
        
        response = self.chatbot.get_response(user_input)
        return str(response)
"""
```

#### `chat_app/chat_service.py`
```python
from .models import ChatHistory
from .bot_manager import BotManager

class ChatService:
    def __init__(self):
        self.bot_manager = BotManager()
    
    def process_message(self, user_message):
        """Process user message and return bot response"""
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
```

#### `chat_app/terminal_client.py`
```python
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')
django.setup()

from chat_app.chat_service import ChatService

class TerminalChatClient:
    def __init__(self):
        self.chat_service = ChatService()
        self.running = True
        
    def display_welcome(self):
        """Display welcome message"""
        print("=" * 60)
        print("🤖 WELCOME TO DJANGO CHATTERBOT TERMINAL CLIENT 🤖")
        print("=" * 60)
        print("Type 'quit', 'exit', or 'bye' to end the conversation")
        print("Type 'history' to see recent chat history")
        print("Type 'clear' to clear the screen")
        print("Type 'help' to show available commands")
        print("-" * 60)
        
    def display_history(self):
        """Display recent chat history"""
        print("\n📜 Recent Chat History:")
        print("-" * 40)
        history = self.chat_service.get_chat_history(5)
        
        if not history:
            print("No chat history found.")
        else:
            for chat in reversed(history):
                print(f"user: {chat.user_message}")
                print(f"bot: {chat.bot_response}")
                print()
        print("-" * 40)
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def handle_special_commands(self, user_input):
        """Handle special terminal commands"""
        user_input_lower = user_input.lower().strip()
        
        if user_input_lower in ['quit', 'exit', 'bye', 'goodbye']:
            print("bot: Goodbye! It was nice chatting with you.")
            self.running = False
            return True
            
        elif user_input_lower == 'history':
            self.display_history()
            return True
            
        elif user_input_lower == 'clear':
            self.clear_screen()
            self.display_welcome()
            return True
            
        elif user_input_lower == 'help':
            self.show_help()
            return True
            
        return False
    
    def show_help(self):
        """Display help information"""
        print("\n🆘 Available Commands:")
        print("- 'quit', 'exit', 'bye': End the conversation")
        print("- 'history': Show recent chat history")
        print("- 'clear': Clear the screen")
        print("- 'help': Show this help message")
        print("- Any other text: Chat with the bot")
        print()
    
    def run(self):
        """Main chat loop"""
        self.display_welcome()
        
        # Initialize bot (this will trigger training if needed)
        print("Initializing bot...")
        self.chat_service.bot_manager.train_bot()
        print("Ready to chat!\n")
        
        while self.running:
            try:
                # Get user input
                user_input = input("user: ").strip()
                
                # Skip empty input
                if not user_input:
                    continue
                
                # Handle special commands
                if self.handle_special_commands(user_input):
                    continue
                
                # Process regular chat message
                print("bot: ", end="", flush=True)
                bot_response = self.chat_service.process_message(user_input)
                print(bot_response)
                
            except KeyboardInterrupt:
                print("\n\nbot: Goodbye! Thanks for chatting.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please try again.")

if __name__ == "__main__":
    client = TerminalChatClient()
    client.run()
```

#### `chat_app/management/commands/start_chat.py`
```python
from django.core.management.base import BaseCommand
from chat_app.terminal_client import TerminalChatClient

class Command(BaseCommand):
    help = 'Start the terminal chat client'
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting Django ChatterBot Terminal Client...')
        )
        client = TerminalChatClient()
        client.run()
```

### Helper Files

#### `run_chat.py` (Project Root)
```python
#!/usr/bin/env python
"""
Direct runner script for the Django ChatterBot Terminal Client
Place this file in your chat_project root directory (same level as manage.py)
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')
django.setup()

# Import and run the terminal client
from chat_app.terminal_client import TerminalChatClient

if __name__ == "__main__":
    print("Starting Django ChatterBot Terminal Client...")
    try:
        client = TerminalChatClient()
        client.run()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you've run migrations: python manage.py migrate")
```

#### `requirements.txt`
```txt
Django>=4.2.0
chatterbot>=1.0.8
chatterbot-corpus>=1.2.0
```

#### `.gitignore`
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# ChatterBot
chatbot_database.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
```

#### `README.md`
```markdown
# Django ChatterBot Terminal Client

A terminal-based chat application using Django and ChatterBot for conversational AI.

## Features
- Interactive terminal chat interface
- Persistent chat history storage
- Machine learning-based responses (or mock responses)
- Special commands (history, clear, help, quit)
- Django admin interface for managing chat history

## Quick Start

1. Install dependencies:
   ```bash
   pip install Django
   # Optional: pip install chatterbot chatterbot-corpus
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Start chatting:
   ```bash
   python run_chat.py
   # OR
   python manage.py start_chat
   ```

## Usage

- Type messages to chat with the bot
- Use 'history' to see recent conversations
- Use 'clear' to clear the screen
- Use 'help' to see available commands
- Use 'quit' to exit

## Sample Conversation

```
user: Good morning! How are you doing?
bot: I am doing very well, thank you for asking.
user: You're welcome.
bot: Do you like hats?
```

## Requirements
- Python 3.7+
- Django 4.2+
- Optional: ChatterBot 1.0.8+ (falls back to mock bot if unavailable)
```

## Usage Instructions

### Running the Application

1. **Using the Django management command:**
   ```bash
   python manage.py start_chat
   ```

2. **Using the direct runner script:**
   ```bash
   python run_chat.py
   ```

### Available Commands

- **Regular chat**: Type any message to chat with the bot
- **`history`**: Display recent chat history
- **`clear`**: Clear the terminal screen
- **`help`**: Show available commands
- **`quit`/`exit`/`bye`**: End the conversation

### Sample Conversation Flow

```
🤖 WELCOME TO DJANGO CHATTERBOT TERMINAL CLIENT 🤖
============================================================
Type 'quit', 'exit', or 'bye' to end the conversation
Type 'history' to see recent chat history
Type 'clear' to clear the screen
Type 'help' to show available commands
------------------------------------------------------------
Initializing bot...
Training the mock bot... Done!
Bot ready! This is a simple mock bot that simulates ChatterBot functionality.
Ready to chat!

user: Good morning! How are you doing?
bot: I am doing very well, thank you for asking.
user: You're welcome.
bot: Do you like hats?
user: Yes, I do!
bot: That's interesting! Tell me more.
user: quit
bot: Goodbye! It was nice chatting with you.
```

### Django Admin Interface

Access the admin interface at `http://localhost:8000/admin/` after:
1. Creating a superuser: `python manage.py createsuperuser`
2. Starting the server: `python manage.py runserver`

## Troubleshooting

### ChatterBot Installation Issues

If ChatterBot fails to install (common on Apple Silicon Macs):
1. The project automatically falls back to a mock bot
2. Mock bot provides similar conversation patterns
3. All functionality remains the same

### Common Issues

1. **"Unknown command: 'start_chat'"**
   - Use `python run_chat.py` instead
   - Ensure management command structure is correct

2. **"Model class doesn't declare an explicit app_label"**
   - Add `app_label = 'chat_app'` to model Meta class
   - Ensure `chat_app` is in `INSTALLED_APPS`

3. **Import errors**
   - Run `python manage.py migrate` first
   - Check that all `__init__.py` files exist

## Customization

### Adding New Bot Responses

Edit `chat_app/bot_manager.py` and modify the `responses` dictionary in `MockChatBot` class.

### Database Schema Changes

1. Modify `chat_app/models.py`
2. Run: `python manage.py makemigrations`
3. Run: `python manage.py migrate`

### Adding New Commands

Modify the `handle_special_commands` method in `chat_app/terminal_client.py`.

## Technical Details

- **Framework**: Django 4.2+
- **Database**: SQLite (default)
- **AI Engine**: ChatterBot or Mock Bot
- **Architecture**: Model-View-Service pattern
- **Storage**: Persistent chat history in database
- **Interface**: Terminal-based with color support

This manifest provides everything needed to create, understand, and customize the Django ChatterBot Terminal Client project.