#!/usr/bin/env python3
"""
Jossie Eyes - Hardware Test Script
Tests all hardware components on Raspberry Pi
"""

import sys
import time
import logging
from typing import Tuple, Optional

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_camera() -> Tuple[bool, str]:
    """Test camera functionality"""
    print("\n📷 Testing Camera...")
    
    try:
        from picamera2 import Picamera2

        cam = Picamera2()
        config = cam.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"})
        cam.configure(config)
        cam.start()
        time.sleep(1)

        frame = cam.capture_array("main")
        cam.stop()

        height, width = frame.shape[:2]

        return True, f"Camera working! Resolution: {width}x{height}"

    except ImportError:
        return False, "picamera2 not installed"
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_audio_output() -> Tuple[bool, str]:
    """Test speaker/audio output"""
    print("\n🔊 Testing Audio Output...")
    
    try:
        import pyaudio
        
        p = pyaudio.PyAudio()
        
        # Check for output devices
        output_devices = []
        for i in range(p.get_device_count()):
            dev_info = p.get_device_info_by_index(i)
            if dev_info['maxOutputChannels'] > 0:
                output_devices.append(dev_info['name'])
        
        p.terminate()
        
        if not output_devices:
            return False, "No audio output devices found"
        
        return True, f"Audio output available! Devices: {', '.join(output_devices[:3])}"
        
    except ImportError:
        return False, "PyAudio not installed (pip install pyaudio)"
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_audio_input() -> Tuple[bool, str]:
    """Test microphone/audio input"""
    print("\n🎤 Testing Audio Input...")
    
    try:
        import pyaudio
        
        p = pyaudio.PyAudio()
        
        # Check for input devices
        input_devices = []
        for i in range(p.get_device_count()):
            dev_info = p.get_device_info_by_index(i)
            if dev_info['maxInputChannels'] > 0:
                input_devices.append(dev_info['name'])
        
        p.terminate()
        
        if not input_devices:
            return False, "No audio input devices found"
        
        return True, f"Audio input available! Devices: {', '.join(input_devices[:3])}"
        
    except ImportError:
        return False, "PyAudio not installed (pip install pyaudio)"
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_gpio() -> Tuple[bool, str]:
    """Test GPIO buttons (optional)"""
    print("\n🔘 Testing GPIO...")
    
    try:
        # Try gpiozero first (better for Pi 5)
        from gpiozero import Button
        
        buttons = {
            17: "Describe",
            27: "OCR",
            22: "Neural"
        }
        
        working_buttons = []
        
        for pin, name in buttons.items():
            try:
                btn = Button(pin, pull_up=True)
                working_buttons.append(f"{name} (GPIO {pin})")
                btn.close()
            except:
                pass
        
        if working_buttons:
            return True, f"GPIO buttons detected: {', '.join(working_buttons)}"
        else:
            return False, "No GPIO buttons detected (this is OK - keyboard input will be used)"
            
    except ImportError:
        return False, "gpiozero not installed (pip install gpiozero)"
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_network() -> Tuple[bool, str]:
    """Test internet connectivity"""
    print("\n🌐 Testing Network...")
    
    try:
        import socket
        
        # Try to connect to Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        
        return True, "Internet connection available"
        
    except Exception as e:
        return False, f"No internet connection: {str(e)}"

def test_env_file() -> Tuple[bool, str]:
    """Test if .env file exists"""
    print("\n📄 Testing Environment Configuration...")
    
    import os
    
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    
    if os.path.exists(env_path):
        # Check if it has required keys
        with open(env_path, 'r') as f:
            content = f.read()
        
        required_keys = ['AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_KEY', 'AZURE_SPEECH_KEY']
        missing_keys = [key for key in required_keys if key not in content]
        
        if missing_keys:
            return False, f".env file exists but missing keys: {', '.join(missing_keys)}"
        
        return True, ".env file configured correctly"
    else:
        return False, ".env file not found (run Azure deployment first)"

def test_python_version() -> Tuple[bool, str]:
    """Test Python version"""
    print("\n🐍 Testing Python Version...")
    
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    if sys.version_info >= (3, 8):
        return True, f"Python {version} (OK)"
    else:
        return False, f"Python {version} (too old, need 3.8+)"

def main():
    """Run all hardware tests"""
    print("=" * 60)
    print("  Jossie Eyes - Hardware Test")
    print("=" * 60)
    
    tests = [
        test_python_version,
        test_camera,
        test_audio_output,
        test_audio_input,
        test_gpio,
        test_network,
        test_env_file
    ]
    
    results = []
    
    for test_func in tests:
        try:
            success, message = test_func()
            results.append((success, message))
            
            status = "✅" if success else "❌"
            print(f"{status} {message}")
            
        except Exception as e:
            results.append((False, str(e)))
            print(f"❌ Error running test: {str(e)}")
        
        time.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 60)
    print("  Test Summary")
    print("=" * 60)
    
    passed = sum(1 for success, _ in results if success)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    # Check if critical components work
    critical_tests = {
        "Python": results[0][0],
        "Camera": results[1][0],
        "Audio Output": results[2][0],
        "Network": results[5][0],
        "Environment": results[6][0]
    }
    
    critical_passed = sum(1 for v in critical_tests.values() if v)
    critical_total = len(critical_tests)
    
    print(f"Critical components: {critical_passed}/{critical_total}")
    
    if critical_passed == critical_total:
        print("\n🎉 System is ready! You can run: python src/edge_device.py")
    else:
        print("\n⚠️  Some critical components are missing. Please fix the issues above.")
        print("   Note: GPIO buttons are optional - keyboard input will work.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()