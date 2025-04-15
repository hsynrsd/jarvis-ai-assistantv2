#!/usr/bin/env python3
"""
J.A.R.V.I.S. - Just A Rather Very Intelligent System
A personal AI assistant inspired by Iron Man's J.A.R.V.I.S.
"""

import os
import sys
import logging
from typing import Dict, Callable, Any
from dotenv import load_dotenv
from commands.context import ContextManager

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Jarvis:
    def __init__(self):
        """Initialize the J.A.R.V.I.S. assistant."""
        self.commands: Dict[str, Callable] = {}
        self.context_manager = ContextManager()
        self.load_environment()
        self.load_commands()
        logger.info("J.A.R.V.I.S. initialized with commands: %s", list(self.commands.keys()))
        
    def load_environment(self):
        """Load environment variables from .env file."""
        load_dotenv()
        # Add your API keys and other configuration here
        
    def load_commands(self):
        """Load and register commands from all modules in the commands package."""
        try:
            logger.debug("Starting to load commands...")
            
            # Import command modules directly
            from commands import web_browser, voice, conversation
            
            # Register commands from each module
            web_browser.register_commands(self)
            voice.register_commands(self)
            conversation.register_commands(self)
            
            # Register context-related commands
            self.register_command("context", self._show_context)
            self.register_command("clear context", self._clear_context)
            
            logger.info(f"Total commands registered: {len(self.commands)}")
            logger.debug(f"Registered commands: {list(self.commands.keys())}")
            
        except Exception as e:
            logger.error(f"Error in load_commands: {e}")
            logger.exception("Full traceback:")
        
    def register_command(self, command: str, handler: Callable):
        """Register a new command handler."""
        self.commands[command.lower()] = handler
        logger.debug(f"Registered command: {command}")
        
    def process_command(self, input_text: str) -> Any:
        """Process user input and execute the appropriate command with context awareness."""
        input_text = input_text.lower().strip()
        logger.debug(f"Processing input: {input_text}")
        
        # Get recent context
        recent_context = self.context_manager.get_recent_context()
        current_context = self.context_manager.get_current_context()
        
        # First try exact command match
        if input_text in self.commands:
            logger.debug(f"Found exact match for command: {input_text}")
            response = self.commands[input_text]("")
            self._update_context(input_text, response, "exact_match")
            return response
            
        # Then try prefix matching for multi-word commands
        for command, handler in self.commands.items():
            if input_text.startswith(command):
                logger.debug(f"Found prefix match for command: {command}")
                remaining_text = input_text[len(command):].strip()
                response = handler(remaining_text)
                self._update_context(input_text, response, "prefix_match")
                return response
        
        # If no command matches, treat it as conversation
        logger.debug("No command match found, treating as conversation")
        try:
            response = self.conversation_handler.get_response(input_text, recent_context)
            self._update_context(input_text, response, "conversation")
            return response
        except Exception as e:
            logger.error(f"Error in conversation handler: {e}")
            return "I'm having trouble with that. Could you try rephrasing?"
    
    def _update_context(self, user_input: str, response: str, command_type: str):
        """Update the conversation context with the latest interaction."""
        self.context_manager.add_turn(user_input, response, command_type)
        logger.debug(f"Updated context with turn: {user_input} -> {response}")
    
    def _show_context(self, _) -> str:
        """Show the current conversation context."""
        return self.context_manager.get_context_summary()
    
    def _clear_context(self, _) -> str:
        """Clear the current conversation context."""
        self.context_manager.clear_context()
        return "Conversation context cleared."
    
    def run(self):
        """Main application loop."""
        print("J.A.R.V.I.S. initialized. Type 'exit' to quit.")
        if self.commands:
            print("Available commands:", ", ".join(self.commands.keys()))
        else:
            print("Warning: No commands were loaded!")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() == 'exit':
                    print("Goodbye!")
                    break
                
                response = self.process_command(user_input)
                print(f"J.A.R.V.I.S.: {response}")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"Error processing command: {e}")
                print("I encountered an error. Please try again.")

def main():
    """Entry point for the application."""
    jarvis = Jarvis()
    jarvis.run()

if __name__ == "__main__":
    main() 