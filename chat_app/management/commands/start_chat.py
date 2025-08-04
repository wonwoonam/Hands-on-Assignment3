from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Start the terminal chat client'
    
    def handle(self, *args, **options):
        self.stdout.write('Starting Django ChatterBot Terminal Client...')
        
        # Import here to avoid issues
        try:
            from chat_app.terminal_client import TerminalChatClient
            client = TerminalChatClient()
            client.run()
        except ImportError as e:
            self.stdout.write(f'Import error: {e}')