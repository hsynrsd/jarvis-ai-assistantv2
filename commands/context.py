"""
Context management module for J.A.R.V.I.S.
Handles conversation history and context-aware command processing.
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ContextManager:
    def __init__(self, max_history: int = 10, context_timeout: int = 300):
        """
        Initialize the context manager.
        
        Args:
            max_history: Maximum number of conversation turns to remember
            context_timeout: Time in seconds before context expires
        """
        self.conversation_history: List[Dict] = []
        self.max_history = max_history
        self.context_timeout = context_timeout
        self.current_context: Optional[Dict] = None
        
    def add_turn(self, user_input: str, assistant_response: str, command_type: str = None):
        """Add a conversation turn to the history."""
        turn = {
            'timestamp': datetime.now(),
            'user_input': user_input,
            'assistant_response': assistant_response,
            'command_type': command_type
        }
        self.conversation_history.append(turn)
        
        # Trim history if it exceeds max_history
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
            
        logger.debug(f"Added conversation turn: {turn}")
        
    def get_recent_context(self, n_turns: int = 3) -> List[Dict]:
        """Get the most recent conversation turns."""
        # Filter out expired context
        self._clean_expired_context()
        return self.conversation_history[-n_turns:] if self.conversation_history else []
        
    def set_current_context(self, context: Dict):
        """Set the current context for the conversation."""
        self.current_context = context
        logger.debug(f"Set current context: {context}")
        
    def get_current_context(self) -> Optional[Dict]:
        """Get the current context."""
        return self.current_context
        
    def clear_context(self):
        """Clear the current context."""
        self.current_context = None
        logger.debug("Cleared current context")
        
    def _clean_expired_context(self):
        """Remove expired conversation turns."""
        now = datetime.now()
        self.conversation_history = [
            turn for turn in self.conversation_history
            if now - turn['timestamp'] < timedelta(seconds=self.context_timeout)
        ]
        
    def get_context_summary(self) -> str:
        """Get a summary of the current conversation context."""
        recent_turns = self.get_recent_context()
        if not recent_turns:
            return "No recent conversation context."
            
        summary = "Recent conversation context:\n"
        for turn in recent_turns:
            summary += f"- User: {turn['user_input']}\n"
            summary += f"  Assistant: {turn['assistant_response']}\n"
            
        if self.current_context:
            summary += f"\nCurrent context: {self.current_context}"
            
        return summary 