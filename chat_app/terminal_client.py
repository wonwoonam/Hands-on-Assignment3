import os
import sys
from .bot_manager import BotManager

class TerminalChatClient:
    def __init__(self):
        self.bot_manager = BotManager()
        self.chat_history = []  # Store in memory instead of database
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_header(self):
        """Print the chat header"""
        print("=" * 60)
        print("🤖 WELCOME TO DJANGO CHATTERBOT TERMINAL CLIENT 🤖")
        print("=" * 60)
        print("Type 'quit', 'exit', or 'bye' to end the conversation")
        print("Type 'history' to see recent chat history")
        print("Type 'clear' to clear the screen")
        print("-" * 60)
        
    def show_history(self):
        """Show recent chat history"""
        if not self.chat_history:
            print("No chat history available.")
            return
            
        print("\n--- Recent Chat History ---")
        for i, (user_msg, bot_msg) in enumerate(self.chat_history[-10:], 1):
            print(f"{i}. User: {user_msg}")
            print(f"   Bot: {bot_msg}")
            print()
            
    def save_to_history(self, user_message, bot_response):
        """Save conversation to memory"""
        self.chat_history.append((user_message, bot_response))
        
    def run(self):
        """Main chat loop"""
        self.print_header()
        
        print("Initializing bot...")
        try:
            self.bot_manager.train_bot()
            print("Ready to chat!")
        except Exception as e:
            print(f"Error initializing bot: {e}")
            return
            
        while True:
            try:
                user_input = input("user: ").strip()
                
                if not user_input:
                    continue
                    
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("bot: Goodbye! Thanks for chatting!")
                    break
                elif user_input.lower() == 'history':
                    self.show_history()
                    continue
                elif user_input.lower() == 'clear':
                    self.clear_screen()
                    self.print_header()
                    continue
                
                # Get bot response
                try:
                    bot_response = self.bot_manager.get_response(user_input)
                    print(f"bot: {bot_response}")
                    
                    # Save to history
                    self.save_to_history(user_input, bot_response)
                    
                except Exception as e:
                    print(f"bot: An error occurred: {e}")
                    print("Please try again.")
                    
            except KeyboardInterrupt:
                print("\nbot: Goodbye! Thanks for chatting!")
                break
            except EOFError:
                print("\nbot: Goodbye! Thanks for chatting!")
                break