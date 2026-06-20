"""
Jossie Eyes - Audio Engine
Handles text-to-speech and audio playback
"""

import os
import io
import logging
import threading
from typing import Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AudioEngine:
    """
    Audio engine for Jossie Eyes
    Handles TTS via Azure Speech Services and local audio playback
    """
    
    def __init__(self):
        """Initialize the audio engine"""
        self.speech_config = None
        self.speech_synthesizer = None
        self.audio_available = False
        
        self._init_azure_speech()
        self._init_local_audio()
    
    def _init_azure_speech(self):
        """Initialize Azure Speech Service"""
        try:
            from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
            
            speech_key = os.getenv('AZURE_SPEECH_KEY')
            speech_region = os.getenv('AZURE_SPEECH_REGION', 'westeurope')
            
            if speech_key:
                self.speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
                # Set voice (neural voice for natural sound)
                self.speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural'
                self.audio_available = True
                logger.info("Azure Speech Service initialized")
            else:
                logger.warning("AZURE_SPEECH_KEY not set - TTS will be limited")
                
        except ImportError:
            logger.warning("Azure Speech SDK not installed - TTS unavailable")
        except Exception as e:
            logger.error(f"Failed to initialize Azure Speech: {e}")
    
    def _init_local_audio(self):
        """Initialize local audio playback capabilities"""
        try:
            import pyaudio
            self.pyaudio = pyaudio
            self.audio_playback_available = True
            logger.info("PyAudio available for local playback")
        except ImportError:
            self.pyaudio = None
            self.audio_playback_available = False
            logger.warning("PyAudio not available - audio playback limited")
    
    def speak(self, text: str, async_mode: bool = True):
        """
        Speak text using Azure TTS
        
        Args:
            text: Text to speak
            async_mode: If True, speak asynchronously
        """
        if not self.speech_config:
            logger.warning("Speech config not available")
            # Fallback: print the text
            print(f"[SPEAK] {text}")
            return
        
        if async_mode:
            # Speak asynchronously
            thread = threading.Thread(target=self._speak_sync, args=(text,))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text)
    
    def _speak_sync(self, text: str):
        """Synchronous speech synthesis and playback"""
        try:
            from azure.cognitiveservices.speech import SpeechSynthesizer, ResultReason
            
            synthesizer = SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == ResultReason.SynthesizingAudioCompleted:
                audio_data = result.audio_data
                if self.audio_playback_available:
                    self._play_audio_data(audio_data)
                else:
                    # Save to file if no playback available
                    filename = f"speech_{int(time.time())}.wav"
                    self._save_audio(audio_data, filename)
                    logger.info(f"Audio saved to {filename}")
            else:
                logger.error(f"Speech synthesis failed: {result.reason}")
                
        except Exception as e:
            logger.error(f"Speech error: {e}")
    
    def _play_audio_data(self, audio_data: bytes):
        """Play audio data through speakers"""
        if not self.pyaudio:
            return
        
        try:
            p = self.pyaudio.PyAudio()
            stream = p.open(format=self.pyaudio.paInt16,
                          channels=1,
                          rate=16000,
                          output=True)
            stream.write(audio_data)
            stream.stop_stream()
            stream.close()
            p.terminate()
        except Exception as e:
            logger.error(f"Audio playback error: {e}")
    
    def _save_audio(self, audio_data: bytes, filename: str):
        """Save audio data to file"""
        import wave
        import time
        
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(audio_data)
        except Exception as e:
            logger.error(f"Failed to save audio: {e}")
    
    def play_sound(self, sound_type: str):
        """
        Play a predefined sound effect
        
        Args:
            sound_type: Type of sound ('offline', 'startup', 'error')
        """
        # For now, just speak a message
        messages = {
            'offline': 'Warning: No internet connection. Some features may be limited.',
            'startup': 'Jossie Eyes started. Press button 1 to describe, 2 to read text, 3 for detailed mode.',
            'error': 'An error occurred. Please try again.'
        }
        
        message = messages.get(sound_type, 'Audio notification')
        self.speak(message)
    
    def stream_speech(self, text: str):
        """
        Stream speech synthesis for lower latency
        
        Args:
            text: Text to synthesize and stream
        """
        if not self.speech_config:
            return
        
        try:
            from azure.cognitiveservices.speech import SpeechSynthesizer, ResultReason
            
            # Use streaming synthesis
            stream = io.BytesIO()
            audio_config = None  # Will use default speaker
            
            synthesizer = SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            # Stream the result
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == ResultReason.SynthesizingAudioCompleted:
                if self.audio_playback_available:
                    self._play_audio_data(result.audio_data)
                    
        except Exception as e:
            logger.error(f"Stream speech error: {e}")


# Simple audio player for testing
def test_audio():
    """Test the audio engine"""
    engine = AudioEngine()
    engine.speak("Hello! Jossie Eyes audio system is working.", async_mode=False)


if __name__ == "__main__":
    test_audio()