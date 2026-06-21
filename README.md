# Jossie Eyes - Neural Sensory Guide

An assistive device for visually impaired individuals that uses Azure AI to describe the world through spatial audio. Built with Raspberry Pi, Azure OpenAI (GPT-4o Vision), and Azure Speech Services.

## 🎯 Project Goal

Jossie Eyes acts as a "Neural Bridge" between visual input and auditory output, helping blind users navigate their surroundings safely and confidently. The device captures images, analyzes them with AI, and provides real-time audio descriptions using spatial positioning (clock-face directions).

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Raspberry Pi   │    │   Azure Cloud    │    │     User        │
│  (Edge Device)  │───▶│  (AI Services)   │───▶│  (Audio Out)    │
│                 │    │                  │    │                 │
│ • Camera        │    │ • GPT-4o Vision  │    │ • Spatial TTS   │
│ • 3 Buttons     │    │ • Speech Service │    │ • 3.5mm Jack    │
│ • OpenCV        │    │ • AI Foundry     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
jossie-eyes/
├── infrastructure/
│   ├── main.bicep              # Main Bicep template (subscription scope)
│   └── resources.bicep         # Resource group module
├── src/
│   ├── brain_service.py        # Azure AI orchestration
│   ├── edge_device.py          # Main Raspberry Pi application
│   ├── button_handler.py       # GPIO button listeners
│   └── audio_engine.py         # Text-to-speech & audio playback
├── scripts/
│   ├── setup_azure.sh          # Azure CLI & Bicep setup
│   ├── deploy_bicep.sh         # Deploy Azure resources
│   └── startup.sh              # Raspberry Pi boot script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- **Azure Subscription** with owner permissions
- **Raspberry Pi** 4 or 5 (for edge device)
- **Python 3.8+** (for development)
- **Camera module** (Pi Camera or USB webcam)

### 2. Deploy Azure Infrastructure

```bash
# Navigate to project
cd jossie-eyes

# Make scripts executable
chmod +x scripts/*.sh

# Setup Azure CLI and login
./scripts/setup_azure.sh

# Deploy Azure resources
./scripts/deploy_bicep.sh
```

This will create:
- Azure OpenAI Service (GPT-4o with vision)
- Azure AI Services (Speech & Computer Vision)
- Azure AI Foundry Hub & Project
- Resource Group: `rg-jossie-eyes`

### 3. Configure Environment

The deployment script automatically creates a `.env` file with your API keys. Verify it contains:

```bash
AZURE_OPENAI_ENDPOINT=https://your-service.openai.azure.com/
AZURE_OPENAI_KEY=your-key
AZURE_SPEECH_KEY=your-speech-key
AZURE_SPEECH_REGION=westeurope
```

### 4. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\Activate   # Windows

# Install packages
pip install -r requirements.txt
```

### 5. Run the Edge Device

```bash
# Start the application
python src/edge_device.py
```

On non-Raspberry Pi systems, it runs in simulation mode with keyboard input:
- Press `1` - Describe Scene
- Press `2` - Read Text (OCR)
- Press `3` - Neural Simulation
- Press `q` - Quit

## 🎮 Usage Modes

### Button 1: Describe Scene
Provides a concise, safety-first description using clock positions:
> "At 12 o'clock, 3 meters ahead, there's an open door. To your right at 3 o'clock, a chair is positioned 1 meter away. The path ahead is clear."

### Button 2: Read Text (OCR)
Reads any visible text in the scene:
> "I see a street sign that reads 'Main Street'. Below it, there's a smaller sign saying 'Speed Limit 30'."

### Button 3: Neural Simulation
Provides an immersive, hyper-detailed sensory description:
> "You're standing in a sunlit room with large windows at 12 o'clock. Warm light streams in, creating patterns on the wooden floor. At 3 o'clock, you can hear the faint hum of a refrigerator. The air carries a subtle scent of coffee from 9 o'clock direction..."

## 🔧 Raspberry Pi Setup

### Hardware Required
- Raspberry Pi 4 or 5 (4GB+ RAM recommended)
- Camera Module v2 or USB webcam
- **Speaker**: 3.5mm audio jack or USB speaker (for audio output)
- **Microphone** (optional): USB microphone (for future voice commands)
- **Buttons** (optional): 3 push buttons + 10kΩ resistors (or use keyboard input)
- WiFi connectivity

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
cd ~
git clone https://github.com/alvinidh/fixathon-josie.git
cd fixathon-josie/jossie-eyes
```

#### 2. Install System Dependencies
```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y python3-pip python3-venv python3-opencv libatlas-base-dev libopenjp2-7 libtiff6 portaudio19-dev
```

#### 3. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

#### 4. Install Python Dependencies
```bash
# Install project requirements
pip install -r requirements.txt

# Install additional packages for Pi (if using GPIO buttons)
pip install RPi.GPIO gpiozero pyaudio
```

#### 5. Configure Audio
```bash
# Check audio devices
aplay -l
arecord -l

# Test speaker
speaker-test -t wav

# If needed, set default audio output by editing /etc/asound.conf
```

#### 6. Set Up Environment Variables
Create a `.env` file in the `jossie-eyes` directory:

```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-service.openai.azure.com/
AZURE_OPENAI_KEY=your_key_here
AZURE_OPENAI_API_VERSION=2024-02-01

# Azure AI Services (Speech)
AZURE_SPEECH_KEY=your_speech_key_here
AZURE_SPEECH_REGION=westeurope
```

*Note: You'll receive the actual values once Azure deployment is complete.*

#### 7. Test the System
```bash
# Run the hardware test script
python src/hardware_test.py

# Run the main application
python src/edge_device.py
```

### 🎮 Input Methods

The system supports multiple input methods:

1. **Keyboard Input** (default, no hardware needed):
   - Press `1` - Describe Scene
   - Press `2` - Read Text (OCR)
   - Press `3` - Neural Simulation
   - Press `q` - Quit

2. **GPIO Buttons** (optional hardware):
   - Wire buttons to GPIO 17, 27, 22
   - System automatically detects and uses them

### GPIO Wiring (Optional)
```
Button 1 (Describe) → GPIO 17 → GND (through 10kΩ pull-up resistor)
Button 2 (OCR)      → GPIO 27 → GND (through 10kΩ pull-up resistor)
Button 3 (Neural)   → GPIO 22 → GND (through 10kΩ pull-up resistor)
```

### Boot on Startup
```bash
# Copy startup script to cron
(crontab -l 2>/dev/null; echo "@reboot cd /home/pi/fixathon-josie/jossie-eyes && source venv/bin/activate && python src/edge_device.py") | crontab -
```

### Troubleshooting

#### Camera Issues:
```bash
# Check camera connection
ls -la /dev/video*

# Test camera
libcamera-hello --timeout 5000
```

#### Audio Issues:
```bash
# List audio devices
aplay -l
arecord -l

# Test speaker
speaker-test -t wav
```

#### Permission Issues:
```bash
# Add user to video group (for camera)
sudo usermod -a -G video $USER

# Add user to audio group
sudo usermod -a -G audio $USER

# Reboot after changes
sudo reboot
```

## 🎯 AI Agent Design

The system uses a specialized "Neural Sensory Guide" agent with these principles:

1. **Safety First**: Always identify hazards before describing the scene
2. **Clock Positions**: Use 12/3/6/9 o'clock for spatial awareness
3. **Actionable**: Provide clear, useful information for navigation
4. **Context Aware**: Adapt descriptions for indoor/outdoor environments
5. **Concise**: Essential information first, details on request

## 🛠️ Development

### Running Tests
```bash
pytest tests/ -v --cov=src
```

### Code Formatting
```bash
black src/
flake8 src/
```

### Local Testing
The application works on any system (not just Raspberry Pi):
- Without GPIO, it uses keyboard input simulation
- Without camera, it uses placeholder images
- Without Azure credentials, it shows helpful error messages

## 🔒 Security

- **Never commit** `.env` files (contains API keys)
- Use Azure Managed Identity in production when possible
- Rotate API keys regularly
- Keep Azure resources in private networks when feasible

## 📊 Azure Costs

Estimated monthly costs (West Europe region):
- Azure OpenAI (GPT-4o): ~$0.03 per 1K tokens
- Azure AI Services (Speech): ~$1 per 1M characters
- Azure AI Foundry: Basic tier (~$20/month)

**Total estimated**: $30-50/month for moderate usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built with:
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- [Azure AI Services](https://azure.microsoft.com/en-us/products/ai-services/ai-services)
- [Azure AI Foundry](https://ai.azure.com/)
- [Raspberry Pi](https://www.raspberrypi.org/)
- [OpenCV](https://opencv.org/)

---

**Jossie Eyes** - Helping visually impaired individuals see the world through AI.