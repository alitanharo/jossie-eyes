"""
Jossie Eyes - Edge Device
Raspberry Pi main application for image capture and processing
"""

import os
import sys
import time
import logging
import threading
from typing import Optional
from dotenv import load_dotenv

# Import our custom modules
from brain_service import BrainService
from button_handler import ButtonHandler
from audio_engine import AudioEngine

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EdgeDevice:
    """
    Main edge device controller for Jossie Eyes
    Manages camera, buttons, and communication with Azure AI services
    """
    
    def __init__(self):
        """Initialize the edge device"""
        self.brain_service = None
        self.audio_engine = None
        self.button_handler = None
        self.camera = None
        self.running = False
        
        # Try to initialize camera
        self._init_camera()
        
        # Initialize services (may fail if no network)
        self._init_services()
    
    def _init_camera(self):
        """Initialize the camera"""
        try:
            import cv2
            self.camera = cv2.VideoCapture(0)
            
            # Set camera properties for better quality
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.camera.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)  # Auto exposure
            
            # Warm up the camera
            time.sleep(2)
            
            logger.info("Camera initialized successfully")
            
        except ImportError:
            logger.warning("OpenCV not available - running in simulation mode")
            self.camera = None
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            self.camera = None
    
    def _init_services(self):
        """Initialize Azure AI services"""
        try:
            self.brain_service = BrainService()
            logger.info("Brain service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize brain service: {e}")
            self.brain_service = None
        
        try:
            self.audio_engine = AudioEngine()
            logger.info("Audio engine initialized")
        except Exception as e:
            logger.error(f"Failed to initialize audio engine: {e}")
            self.audio_engine = None
    
    def capture_image(self) -> Optional[bytes]:
        """
        Capture an image from the camera
        
        Returns:
            Image bytes or None if failed
        """
        if not self.camera:
            logger.warning("Camera not available - using placeholder image")
            # Return a placeholder or test image
            try:
                with open('test_image.jpg', 'rb') as f:
                    return f.read()
            except:
                return None
        
        # Capture multiple frames to ensure good quality
        for _ in range(5):
            ret, frame = self.camera.read()
            if not ret:
                continue
        
        # Capture the actual image
        ret, frame = self.camera.read()
        if not ret:
            logger.error("Failed to capture image")
            return None
        
        # Encode to JPEG
        import cv2
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
        _, buffer = cv2.imencode('.jpg', frame, encode_param)
        
        return buffer.tobytes()
    
    def process_scene(self, mode: str = 'describe'):
        """
        Process a scene: capture image, analyze, and speak description
        
        Args:
            mode: 'describe', 'ocr', or 'neural_simulation'
        """
        if not self.brain_service:
            self.speak_error("AI services not available. Please check your connection.")
            return
        
        # Announce processing
        if self.audio_engine:
            self.audio_engine.speak("Processing scene...")
        
        # Capture image
        logger.info(f"Capturing image for {mode} mode")
        image_data = self.capture_image()
        
        if not image_data:
            self.speak_error("Failed to capture image.")
            return
        
        # Analyze with AI
        logger.info("Analyzing image with Azure AI")
        result = self.brain_service.analyze_image(image_data, mode)
        
        if result['success']:
            description = result['description']
            logger.info(f"Analysis complete: {description[:100]}...")
            
            # Speak the description
            if self.audio_engine:
                self.audio_engine.speak(description)
        else:
            error_msg = result.get('error', 'Unknown error')
            logger.error(f"Analysis failed: {error_msg}")
            self.speak_error("Failed to analyze the scene.")
    
    def speak_error(self, message: str):
        """Speak an error message"""
        if self.audio_engine:
            self.audio_engine.speak(message)
        else:
            logger.error(message)
    
    def check_connectivity(self) -> bool:
        """Check if we have internet connectivity"""
        import socket
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except:
            return False
    
    def start(self):
        """Start the edge device"""
        self.running = True
        
        # Check connectivity
        if not self.check_connectivity():
            logger.warning("No internet connectivity - some features may be limited")
            if self.audio_engine:
                self.audio_engine.play_sound('offline')
        
        # Initialize button handler
        try:
            self.button_handler = ButtonHandler(self)
            self.button_handler.start()
            logger.info("Button handler started")
        except Exception as e:
            logger.error(f"Failed to start button handler: {e}")
        
        logger.info("Jossie Eyes edge device started")
        
        # Keep the main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            self.stop()
    
    def stop(self):
        """Stop the edge device"""
        self.running = False
        
        if self.button_handler:
            self.button_handler.stop()
        
        if self.camera:
            self.camera.release()
        
        logger.info("Jossie Eyes stopped")


def main():
    """Main entry point"""
    print("=" * 50)
    print("  Jossie Eyes - Neural Sensory Guide")
    print("=" * 50)
    print()
    
    device = EdgeDevice()
    
    try:
        device.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
        device.stop()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()