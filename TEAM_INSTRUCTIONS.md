# Jossie Eyes - Hardware Team Instructions

## 🎯 What is Jossie Eyes?

An assistive device for visually impaired individuals that:
- Captures images with a camera
- Analyzes scenes using Azure AI (GPT-4o Vision)
- Provides audio descriptions through a speaker
- Uses keyboard input (or optional GPIO buttons) for mode selection

## 📦 What You Need

### Hardware (Already Available):
- ✅ Raspberry Pi 5 (8GB)
- ✅ Camera module (CSI port)

### Hardware (To Add):
- **Speaker**: 3.5mm audio jack or USB speaker
- **Microphone** (optional): USB microphone
- **Buttons** (optional): 3 push buttons + 10kΩ resistors

## 🚀 Step-by-Step Setup

### Step 1: Connect to Raspberry Pi

Use the remote access:
1. Go to: https://connect.raspberrypi.com
2. Login with:
   - Email: alvin.idh@gmail.com
   - Password: %SZ7s*wq-?S_NRT
3. Click on the Pi to open a shell

### Step 2: Clone the Repository

```bash
cd ~
git clone https://github.com/alvinidh/fixathon-josie.git
cd fixathon-josie/jossie-eyes
```

### Step 3: Install System Dependencies

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y python3-pip python3-venv python3-opencv libatlas-base-dev libopenjp2-7 libtiff6 portaudio19-dev
```

### Step 4: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Step 5: Install Python Dependencies

```bash
# Install project requirements
pip install -r requirements.txt

# Install additional packages for Pi
pip install RPi.GPIO gpiozero pyaudio
```

### Step 6: Configure Audio

```bash
# Check audio devices
aplay -l
arecord -l

# Test speaker
speaker-test -t wav
```

### Step 7: Set Up Environment Variables

Create a `.env` file in the `jossie-eyes` directory with your Azure credentials (you'll receive these from the software team):

```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-service.openai.azure.com/
AZURE_OPENAI_KEY=your_key_here
AZURE_OPENAI_API_VERSION=2024-02-01

# Azure AI Services (Speech)
AZURE_SPEECH_KEY=your_speech_key_here
AZURE_SPEECH_REGION=westeurope
```

### Step 8: Test the System

```bash
# Run the hardware test script
python src/hardware_test.py

# Run the main application
python src/edge_device.py
```

## ⌨️ How to Use

Once running, use these keyboard keys:
- **1**: Describe Scene (safety-first description with clock positions)
- **2**: Read Text (OCR mode)
- **3**: Neural Simulation (detailed immersive description)
- **Q**: Quit

The system will:
1. Capture an image from the camera
2. Send it to Azure AI for analysis
3. Speak the description through the speaker

## 🔧 Troubleshooting

### Camera Issues:
```bash
# Check camera connection
ls -la /dev/video*

# Test camera
libcamera-hello --timeout 5000
```

### Audio Issues:
```bash
# List audio devices
aplay -l
arecord -l

# Test speaker
speaker-test -t wav
```

### Permission Issues:
```bash
# Add user to video group (for camera)
sudo usermod -a -G video $USER

# Add user to audio group
sudo usermod -a -G audio $USER

# Reboot after changes
sudo reboot
```

## 📞 Contact

If you encounter any issues, please contact the software team with:
1. Output of `python src/hardware_test.py`
2. Any error messages
3. Description of what you were trying to do

---

**Good luck with the setup!** 🎉