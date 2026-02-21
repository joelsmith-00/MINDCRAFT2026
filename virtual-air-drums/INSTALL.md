# 📦 Installation Guide - Virtual Air Drums

## Prerequisites

### 1. Install Python
If you don't have Python installed:

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. ✅ **IMPORTANT:** Check "Add Python to PATH" during installation
4. Verify installation: Open Command Prompt and type `python --version`

**macOS:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

## Installation Steps

### Option 1: Automatic Installation (Recommended)

1. **Open Command Prompt/Terminal** in the project folder
   - Windows: Right-click folder → "Open in Terminal" or "Open PowerShell window here"
   - macOS/Linux: Right-click folder → "Open Terminal here"

2. **Install dependencies:**
   ```bash
   python -m pip install opencv-python mediapipe pygame numpy scipy
   ```

3. **Generate drum sounds:**
   ```bash
   python setup_sounds.py
   ```

4. **Run the application:**
   ```bash
   python air_drums.py
   ```

### Option 2: Manual Installation

If the automatic installation doesn't work:

1. **Install each package individually:**
   ```bash
   python -m pip install opencv-python
   python -m pip install mediapipe
   python -m pip install pygame
   python -m pip install numpy
   python -m pip install scipy
   ```

2. **Create sounds folder manually:**
   - Create a folder named `sounds` in the project directory
   - Download free drum samples (WAV format) from:
     - [FreeSound.org](https://freesound.org/)
     - [SampleFocus.com](https://samplefocus.com/)
   - Name them: `hihat.wav`, `snare.wav`, `bass.wav`
   - Place them in the `sounds` folder

3. **Run the application:**
   ```bash
   python air_drums.py
   ```

### Option 3: Using Virtual Environment (Advanced)

For a clean installation:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
python -m pip install -r requirements.txt

# Generate sounds
python setup_sounds.py

# Run application
python air_drums.py
```

## Troubleshooting Installation

### "Python not found" Error
- Make sure Python is installed
- Add Python to PATH (Windows)
- Try `python3` instead of `python`
- Try `py` instead of `python` (Windows)

### "pip not found" Error
- Use `python -m pip` instead of `pip`
- Reinstall Python with "Add to PATH" checked

### Package Installation Fails
- Update pip: `python -m pip install --upgrade pip`
- Install Visual C++ Build Tools (Windows) if needed
- Try installing packages one by one

### Camera Permission Issues
- Grant camera access in system settings
- Close other apps using the camera
- Restart your computer

### Sound Issues
- Make sure sound files are in WAV format
- Check file names are exactly: `hihat.wav`, `snare.wav`, `bass.wav`
- Verify files are in the `sounds` folder

## Verify Installation

Run this command to check if everything is installed:

```bash
python -c "import cv2, mediapipe, pygame, numpy; print('✅ All packages installed successfully!')"
```

If you see the success message, you're ready to go! 🎉

## Next Steps

Once installation is complete:
1. Read `QUICKSTART.md` for usage instructions
2. Run `python air_drums.py` to start playing
3. Have fun! 🥁

## Need Help?

If you're still having issues:
1. Check that Python 3.8+ is installed
2. Make sure all packages are installed
3. Verify your webcam is working
4. Check the `README.md` for more detailed troubleshooting

---

**Ready to drum? Run `python air_drums.py` and start playing! 🎵**
