# 🎯 Jossie Eyes - Raspberry Pi 5 Complete Setup Guide

**For Hardware Team** - Updated: June 21, 2026

---

## 📋 What's New

✅ **Code Updated for Raspberry Pi 5**
- Added gpiozero support (preferred for Pi 5)
- Keyboard input works without GPIO buttons
- Hardware test script to verify all components
- Comprehensive README with troubleshooting

✅ **No Physical Buttons Required**
- System works with keyboard input (1, 2, 3, Q)
- GPIO buttons are optional (can be added later)
- Perfect for testing and development

---

## 🚀 Quick Setup (8 Steps)

### Step 1: Connect to Raspberry Pi
```
URL: https://connect.raspberrypi.com
Email: alvin.idh@gmail.com
Password: %SZ7s*wq-?S_NRT
```

### Step 2: Clone Repository
```bash
cd ~
git clone https://github.com/alvinidh/fixathon-josie.git
cd fixathon-josie/jossie-eyes
```

### Step 3: Install System Dependencies
```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python3-pip python3-venv python3-opencv libatlas-base-dev libopenjp2-7 libtiff6 portaudio19-dev
```

### Step 4: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### Step 5: Install Python Dependencies
```bash
pip install -r requirements.txt
pip install RPi.GPIO gpiozero pyaudio
```

### Step 6: Connect Hardware
- **Speaker**: Connect to 3.5mm jack or USB
- **Camera**: Already connected (CSI port)
- **Microphone** (optional): USB microphone

### Step 7: Configure Environment
Create `.env` file (you'll receive values from software team):
```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-service.openai.azure.com/
AZURE_OPENAI_KEY=your_key_here
AZURE_OPENAI_API_VERSION=2024-02-01

# Azure AI Services (Speech)
AZURE_SPEECH_KEY=your_speech_key_here
AZURE_SPEECH_REGION=westeurope
```

### Step 8: Test Everything
```bash
# Run hardware test
python src/hardware_test.py

# Run the application
python src/edge_device.py
```

---

## ⌨️ How to Use

Once running, use keyboard keys:
- **1**: Describe Scene (safety-first with clock positions)
- **2**: Read Text (OCR mode)
- **3**: Neural Simulation (detailed immersive description)
- **Q**: Quit

The system will:
1. Capture image from camera
2. Send to Azure AI for analysis
3. Speak description through speaker

---

## 🔧 Troubleshooting

### Camera Not Working
```bash
# Check connection
ls -la /dev/video*

# Test camera
libcamera-hello --timeout 5000

# Fix permissions
sudo usermod -a -G video $USER
sudo reboot
```

### Audio Not Working
```bash
# List audio devices
aplay -l
arecord -l

# Test speaker
speaker-test -t wav

# Fix permissions
sudo usermod -a -G audio $USER
sudo reboot
```

### Import Errors
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Permission Denied
```bash
# Add user to groups
sudo usermod -a -G video $USER
sudo usermod -a -G audio $USER
sudo reboot
```

---

## 📦 What's Included

### New Files
- `TEAM_INSTRUCTIONS.md` - Detailed team guide
- `src/hardware_test.py` - Hardware testing script
- `PI_SETUP_GUIDE.md` - This file

### Updated Files
- `README.md` - Complete setup instructions
- `src/button_handler.py` - Added gpiozero support
- `infrastructure/main.bicep` - Updated for new subscription
- `infrastructure/resources.bicep` - Fixed SKU issues

---

## 📞 Need Help?

If you encounter issues, please provide:
1. Output of `python src/hardware_test.py`
2. Any error messages
3. What you were trying to do

---

## ✅ Checklist

Before running the application, ensure:
- [ ] All system dependencies installed
- [ ] Virtual environment created and activated
- [ ] Python dependencies installed
- [ ] Speaker connected and working
- [ ] Camera working (test with `libcamera-hello`)
- [ ] `.env` file created with Azure credentials
- [ ] Hardware test passes (`python src/hardware_test.py`)

---

**🎉 You're ready to go! Run `python src/edge_device.py` to start.**