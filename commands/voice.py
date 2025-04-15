"""
Voice command module for J.A.R.V.I.S.
Handles speech recognition and text-to-speech functionality.
"""

import logging
import threading
import time
import os
import tempfile
from gtts import gTTS
import speech_recognition as sr
import pygame

logger = logging.getLogger(__name__)

class VoiceHandler:
    def __init__(self):
        """Initialize voice recognition and text-to-speech engines."""
        self.voice_enabled = False
        self.is_listening = False
        self.voice_thread = None
        
        try:
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            
            # Initialize pygame for audio playback
            pygame.mixer.init()
            
            self.voice_enabled = True
            logger.info("Voice handler initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize voice handler: {e}")
    
    def speak(self, text: str):
        """Convert text to speech using gTTS."""
        if not self.voice_enabled:
            return "Voice features are not available"
            
        try:
            logger.debug(f"Speaking: {text}")
            
            # Create a temporary file for the audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_filename = temp_file.name
            
            # Generate speech using gTTS
            tts = gTTS(text=text, lang='en')
            tts.save(temp_filename)
            
            # Play the audio
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Clean up
            pygame.mixer.music.unload()
            os.unlink(temp_filename)
            
            return f"Said: {text}"
        except Exception as e:
            logger.error(f"TTS Error: {e}")
            return f"Error speaking: {e}"
    
    def listen_for_wake_word(self, source):
        """Listen for the wake word 'jarvis'."""
        try:
            logger.debug("Listening for wake word...")
            audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=3)
            text = self.recognizer.recognize_google(audio).lower()
            logger.info(f"Heard: {text}")
            return "jarvis" in text
        except sr.WaitTimeoutError:
            return False
        except sr.UnknownValueError:
            return False
        except Exception as e:
            logger.error(f"Error listening for wake word: {e}")
            return False
    
    def listen_for_command(self, source):
        """Listen for a command after wake word."""
        try:
            logger.debug("Starting command capture...")
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            logger.debug("Audio captured, attempting recognition...")
            command = self.recognizer.recognize_google(audio).lower()
            logger.info(f"Command recognized: {command}")
            return command
        except sr.WaitTimeoutError:
            logger.warning("Timeout waiting for command")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand command")
            return None
        except Exception as e:
            logger.error(f"Error listening for command: {e}")
            return None
    
    def start_listening(self, jarvis):
        """Start the voice recognition loop."""
        if not self.voice_enabled:
            return "Voice features are not available"
            
        if self.is_listening:
            return "Already listening"
            
        self.is_listening = True
        self.voice_thread = threading.Thread(target=self._listen_loop, args=(jarvis,))
        self.voice_thread.daemon = True
        self.voice_thread.start()
        return "Voice recognition activated. Say 'Jarvis' to begin."
    
    def stop_listening(self):
        """Stop the voice recognition loop."""
        if not self.voice_enabled:
            return "Voice features are not available"
            
        if self.is_listening:
            self.is_listening = False
            if self.voice_thread:
                self.voice_thread.join()
            return "Voice recognition deactivated"
        return "Not currently listening"
    
    def _listen_loop(self, jarvis):
        """Main voice recognition loop."""
        logger.info("Starting voice recognition loop")
        
        with sr.Microphone() as source:
            # Initial noise adjustment
            logger.info("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while self.is_listening:
                try:
                    # Listen for wake word
                    if self.listen_for_wake_word(source):
                        logger.info("Wake word detected")
                        self.speak("Yes?")
                        
                        # Wait for TTS to finish and let mic calm down
                        logger.debug("Waiting for TTS to finish...")
                        time.sleep(1.5)
                        
                        # Re-adjust for ambient noise before command
                        logger.info("Adjusting for ambient noise before command...")
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        
                        # Listen for command
                        logger.info("Listening for command...")
                        command = self.listen_for_command(source)
                        
                        if command:
                            logger.info(f"Processing command: {command}")
                            response = jarvis.process_command(command)
                            if response:
                                logger.info(f"Command response: {response}")
                                self.speak(response)
                            else:
                                logger.warning("No response from command processing")
                                self.speak("I didn't understand that command")
                        else:
                            logger.warning("No command detected")
                            self.speak("I didn't hear a command")
                            
                except Exception as e:
                    logger.error(f"Error in listen loop: {e}")
                    time.sleep(1)  # Prevent tight error loops

def register_commands(jarvis):
    """Register voice-related commands with J.A.R.V.I.S."""
    try:
        voice_handler = VoiceHandler()
        jarvis.voice_handler = voice_handler
        
        jarvis.register_command("listen", lambda _: voice_handler.start_listening(jarvis))
        jarvis.register_command("stop listening", lambda _: voice_handler.stop_listening())
        jarvis.register_command("speak", lambda text: voice_handler.speak(text))
        
        logger.info("Voice commands registered")
    except Exception as e:
        logger.error(f"Failed to register voice commands: {e}")
