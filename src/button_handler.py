"""
Jossie Eyes - Button Handler
GPIO button listeners for Raspberry Pi
"""

import logging
import threading
import time
from typing import Callable, Optional

logger = logging.getLogger(__name__)

class ButtonHandler:
    """
    Handles GPIO button inputs for Jossie Eyes
    Three buttons for different modes:
    - Button 1 (GPIO 17): Describe Scene
    - Button 2 (GPIO 27): Read Text (OCR)
    - Button 3 (GPIO 22): Neural Simulation
    """
    
    # GPIO pin assignments
    BUTTON_DESCRIBE = 17      # Describe scene mode
    BUTTON_OCR = 27           # Text/OCR mode
    BUTTON_NEURAL = 22        # Neural simulation mode
    
    def __init__(self, edge_device):
        """
        Initialize button handler
        
        Args:
            edge_device: Reference to the EdgeDevice instance
        """
        self.edge_device = edge_device
        self.running = False
        self.buttons = []
        self.debounce_time = 0.3  # seconds
        
        # Try to import RPi.GPIO
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            self.gpio_available = True
            logger.info("RPi.GPIO available")
        except ImportError:
            logger.warning("RPi.GPIO not available - using keyboard simulation mode")
            self.GPIO = None
            self.gpio_available = False
    
    def setup_gpio(self):
        """Setup GPIO pins for buttons"""
        if not self.gpio_available:
            return
        
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setup(self.BUTTON_DESCRIBE, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
        self.GPIO.setup(self.BUTTON_OCR, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
        self.GPIO.setup(self.BUTTON_NEURAL, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
        
        # Add event detection for buttons
        self.GPIO.add_event_detect(
            self.BUTTON_DESCRIBE, 
            self.GPIO.FALLING, 
            callback=self._on_describe_pressed, 
            bouncetime=300
        )
        self.GPIO.add_event_detect(
            self.BUTTON_OCR, 
            self.GPIO.FALLING, 
            callback=self._on_ocr_pressed, 
            bouncetime=300
        )
        self.GPIO.add_event_detect(
            self.BUTTON_NEURAL, 
            self.GPIO.FALLING, 
            callback=self._on_neural_pressed, 
            bouncetime=300
        )
        
        logger.info(f"GPIO buttons configured: Describe(17), OCR(27), Neural(22)")
    
    def _on_describe_pressed(self, channel):
        """Callback for describe button"""
        logger.info("Describe button pressed")
        threading.Thread(target=self._process_button, args=('describe',)).start()
    
    def _on_ocr_pressed(self, channel):
        """Callback for OCR button"""
        logger.info("OCR button pressed")
        threading.Thread(target=self._process_button, args=('ocr',)).start()
    
    def _on_neural_pressed(self, channel):
        """Callback for neural simulation button"""
        logger.info("Neural simulation button pressed")
        threading.Thread(target=self._process_button, args=('neural_simulation',)).start()
    
    def _process_button(self, mode: str):
        """
        Process button press
        
        Args:
            mode: The processing mode to use
        """
        # Announce the mode
        mode_names = {
            'describe': 'Describing scene',
            'ocr': 'Reading text',
            'neural_simulation': 'Neural simulation mode'
        }
        
        if self.edge_device.audio_engine:
            self.edge_device.audio_engine.speak(mode_names.get(mode, 'Processing'))
        
        # Process the scene
        self.edge_device.process_scene(mode)
    
    def start(self):
        """Start the button handler"""
        self.running = True
        
        if self.gpio_available:
            self.setup_gpio()
            logger.info("GPIO button handler started")
        else:
            # Start keyboard input thread for testing
            keyboard_thread = threading.Thread(target=self._keyboard_input_loop)
            keyboard_thread.daemon = True
            keyboard_thread.start()
            logger.info("Keyboard input handler started (simulation mode)")
    
    def _keyboard_input_loop(self):
        """Simulate button presses via keyboard for testing"""
        print("\n=== Button Simulation Mode ===")
        print("Press 1: Describe Scene")
        print("Press 2: Read Text (OCR)")
        print("Press 3: Neural Simulation")
        print("Press q: Quit")
        print("=" * 30)
        
        while self.running:
            try:
                # Non-blocking keyboard input
                import sys
                import select
                import tty
                import termios
                
                # Check if input is available
                if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                    # Read the input
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    try:
                        tty.setraw(fd)
                        ch = sys.stdin.read(1)
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    
                    if ch == '1':
                        self._on_describe_pressed(None)
                    elif ch == '2':
                        self._on_ocr_pressed(None)
                    elif ch == '3':
                        self._on_neural_pressed(None)
                    elif ch == 'q':
                        self.running = False
                        break
                        
            except Exception:
                # If keyboard input fails, just sleep
                time.sleep(0.5)
    
    def stop(self):
        """Stop the button handler"""
        self.running = False
        
        if self.GPIO and self.gpio_available:
            self.GPIO.cleanup()
            logger.info("GPIO cleaned up")
        
        logger.info("Button handler stopped")