"""
Conversation handler for J.A.R.V.I.S.
Handles natural language conversations using OpenRouter's API.
"""

import os
import logging
import requests
import json
from typing import List, Dict

logger = logging.getLogger(__name__)

class ConversationHandler:
    def __init__(self):
        """Initialize the conversation handler."""
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            logger.error("OPENROUTER_API_KEY not found in environment variables")
            raise ValueError("OPENROUTER_API_KEY not found")
            
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.system_prompt = """You are J.A.R.V.I.S., a sophisticated AI assistant inspired by Iron Man's AI.
Your responses should be helpful, direct, and slightly witty - similar to the J.A.R.V.I.S. from Iron Man.
You can engage in natural conversation while also helping with tasks."""
        
    def get_response(self, user_input: str, conversation_history: List[Dict]) -> str:
        """Get a response from OpenRouter using conversation context."""
        try:
            # Convert conversation history to messages format
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history
            for turn in conversation_history:
                messages.append({"role": "user", "content": turn['user_input']})
                messages.append({"role": "assistant", "content": turn['assistant_response']})
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})
            
            # Prepare the request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/hsynrsd/jarvis-ai-assistantv2",  # Update with your repo URL
                "X-Title": "J.A.R.V.I.S. AI Assistant",
                "User-Agent": "J.A.R.V.I.S. AI Assistant/1.0"
            }
            
            data = {
                "model": "deepseek/deepseek-v3-base:free",
                "messages": messages,
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            # Make request to OpenRouter API
            logger.debug(f"Attempting to connect to OpenRouter API")
            response = requests.post(self.api_url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {e}")
            if isinstance(e, requests.exceptions.ConnectionError):
                return "I'm having trouble connecting to my language processing service. Please check your internet connection."
            elif isinstance(e, requests.exceptions.Timeout):
                return "The request to my language processing service timed out. Please try again."
            else:
                return "I'm having trouble connecting to my language processing service."
        except Exception as e:
            logger.error(f"Error in conversation handler: {e}")
            return "I apologize, but I'm having trouble processing that request."
            
def register_commands(jarvis):
    """Register conversation-related commands with J.A.R.V.I.S."""
    try:
        conversation_handler = ConversationHandler()
        jarvis.conversation_handler = conversation_handler
        logger.info("Conversation handler registered with OpenRouter")
    except Exception as e:
        logger.error(f"Failed to register conversation handler: {e}") 