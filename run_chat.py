import os
import django
import yaml
import nltk

# Download required NLTK data
print("Checking NLTK data...")
try:
    nltk.download('punkt_tab', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    print(f"NLTK download warning: {e}")

# Monkey patch to fix PyYAML loader issue
original_load = yaml.load
def patched_load(stream, Loader=yaml.FullLoader):
    return original_load(stream, Loader=Loader)
yaml.load = patched_load

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')
django.setup()

# Now import and run
try:
    from chat_app.terminal_client import TerminalChatClient
    print("Starting Django ChatterBot Terminal Client...")
    client = TerminalChatClient()
    client.run()
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Error: {e}")