# Jossie Eyes - Quick Start Guide

## 🚀 Deploy in 5 Minutes

### Step 1: Setup Azure CLI (One-time)
```bash
cd jossie-eyes
chmod +x scripts/*.sh
./scripts/setup_azure.sh
```

### Step 2: Deploy Azure Resources
```bash
./scripts/deploy_bicep.sh
```
⏱️ This takes 10-15 minutes. Go grab a coffee! ☕

### Step 3: Install Python Dependencies
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\Activate   # Windows
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python src/edge_device.py
```

### Step 5: Test It!
Press keys (or GPIO buttons on Raspberry Pi):
- `1` - Describe the scene
- `2` - Read text (OCR)
- `3` - Neural simulation mode
- `q` - Quit

## 📋 What You Get

After deployment, you'll have:
- ✅ Azure OpenAI Service (GPT-4o with vision)
- ✅ Azure AI Services (Speech & Computer Vision)
- ✅ Resource Group: `rg-jossie-eyes`
- ✅ `.env` file with your API keys

## 🛠️ Troubleshooting

### "Azure CLI not found"
Run `./scripts/setup_azure.sh` to install it.

### "Not logged in"
Run `az login` and follow the prompts.

### "Module not found" errors
Make sure you activated the virtual environment:
```bash
source venv/bin/activate
```

### No camera available
The app runs in simulation mode and uses placeholder images.

## 📱 Raspberry Pi Setup

### Install on Raspberry Pi
```bash
# Clone the repository
git clone https://github.com/alitanharo/jossie-eyes.git
cd jossie-eyes

# Follow steps 1-4 above
```

### Wire the Buttons
```
Button 1 → GPIO 17 (Describe)
Button 2 → GPIO 27 (OCR)
Button 3 → GPIO 22 (Neural)
All buttons → GND (with 10kΩ pull-up resistors)
```

### Run on Boot
```bash
(crontab -l 2>/dev/null; echo "@reboot /home/pi/jossie-eyes/scripts/startup.sh") | crontab -
```

## 🎯 Next Steps

1. **Test with real images**: Point your camera at objects and press button 1
2. **Try OCR mode**: Hold up text (signs, labels) and press button 2
3. **Experience Neural Simulation**: Press button 3 for immersive descriptions

## 💡 Tips

- **Good lighting** improves image quality
- **Hold steady** for a moment while capturing
- **Speak clearly** when testing audio output
- **Check WiFi** if you get connection errors

## 📞 Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review logs in `jossie-eyes.log` (on Raspberry Pi)
- Ensure your Azure subscription is active

---

**Enjoy Jossie Eyes!** 👁️