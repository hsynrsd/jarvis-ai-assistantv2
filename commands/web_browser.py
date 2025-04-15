"""
Web browser command module for J.A.R.V.I.S.
Handles opening websites and web-related tasks.
"""

import webbrowser
import logging

logger = logging.getLogger(__name__)

def open_website(url: str) -> str:
    """Open a website in the default browser."""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        webbrowser.open(url)
        return f"Opening {url}"
    except Exception as e:
        logger.error(f"Error opening website: {e}")
        return "I couldn't open that website. Please check the URL and try again."

def register_commands(jarvis):
    """Register web-related commands with J.A.R.V.I.S."""
    try:
        jarvis.register_command("open", lambda args: open_website(args))
        jarvis.register_command("browse", lambda args: open_website(args))
        logger.info("Web browser commands registered")
    except Exception as e:
        logger.error(f"Error registering web browser commands: {e}") 