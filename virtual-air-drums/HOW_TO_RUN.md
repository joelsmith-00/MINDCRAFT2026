# 🎮 HOW TO RUN - Virtual Air Drums

## ⚠️ Python Setup Required

It looks like Python isn't currently set up in your command line. Here's how to fix that:

---

## 🔧 Step 1: Install Python (If Not Installed)

### Option A: Install from Microsoft Store (Easiest for Windows)
1. Press `Windows Key`
2. Type "Python" and press Enter
3. Windows will open the Microsoft Store
4. Click "Get" to install Python 3.12 (or latest version)
5. Wait for installation to complete

### Option B: Install from Python.org
1. Go to https://python.org/downloads
2. Download Python 3.8 or higher
3. Run the installer
4. ✅ **IMPORTANT:** Check "Add Python to PATH" during installation
5. Complete the installation

---

## 🚀 Step 2: Install Dependencies

Once Python is installed, open a **new** PowerShell or Command Prompt window:

```powershell
# Navigate to the project folder
cd C:\Users\joelm\.gemini\antigravity\scratch\virtual-air-drums

# Install required packages
python -m pip install opencv-python mediapipe pygame numpy scipy
```

**Or use the batch file:**
```powershell
# Just double-click this file in Windows Explorer:
setup.bat
```

---

## 🎵 Step 3: Generate Drum Sounds

```powershell
python setup_sounds.py
```

You should see:
```
✅ Created 'sounds' folder
🎵 Generating hi-hat sound...
🎵 Generating snare sound...
🎵 Generating bass drum sound...
✅ All drum sounds generated successfully!
```

---

## 🥁 Step 4: Run the Application

```powershell
python air_drums.py
```

**Or use the batch file:**
```powershell
# Just double-click this file in Windows Explorer:
run_drums.bat
```

---

## 🎬 What You'll See When Running

### Application Window:
```
┌─────────────────────────────────────────────────────────┐
│ Virtual Air Drums                                   [X] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  FPS: 60                                                │
│                                                         │
│  ┌─────────────────────┬─────────────────────┐        │
│  │                     │                     │        │
│  │   🔴 HI-HAT         │   🟢 SNARE          │        │
│  │                     │                     │        │
│  │  [Your hand here]   │                     │        │
│  │        ✋           │                     │        │
│  └─────────────────────┴─────────────────────┘        │
│  ┌───────────────────────────────────────────┐        │
│  │                                           │        │
│  │         🔵 BASS DRUM                      │        │
│  │                                           │        │
│  └───────────────────────────────────────────┘        │
│                                                         │
│  Virtual Air Drums - Move your hands to play!          │
│  Fast downward motion = Hit                             │
│  Speed = Volume                                         │
│  Press 'Q' to quit                                      │
└─────────────────────────────────────────────────────────┘
```

### What Happens:
1. **Camera turns on** - You'll see yourself in the window
2. **Colored zones appear** - Red (Hi-Hat), Green (Snare), Blue (Bass)
3. **Raise your hands** - Green skeleton lines appear on your hands
4. **Colored circles** follow your index fingers
5. **Make downward motions** - Zones light up and play sounds!

---

## 🎮 How to Play

1. **Position yourself** 2-3 feet from webcam
2. **Raise hands** in front of camera
3. **Move hand over a colored zone**
4. **Make quick DOWNWARD motion** (like hitting a drum)
5. **Hear the sound!** 🎵

### Tips:
- ✅ Quick downward motions work best
- ✅ Faster movement = Louder sound
- ✅ Use both hands for complex beats
- ❌ Don't move too slowly
- ❌ Don't just hover (must move down)

---

## 🎯 Expected Behavior

### When Working Correctly:
- ✅ Camera window opens showing live video
- ✅ Three colored zones are visible
- ✅ Hand skeleton appears when hands detected
- ✅ Colored circles follow your index fingers
- ✅ Zones flash brighter when hit
- ✅ Drum sounds play instantly
- ✅ FPS counter shows 30-60 FPS

### Console Output:
```
🥁 Virtual Air Drums System Starting...
📹 Camera initialized
🎵 Drum zones created
✋ Hand detection ready

Move your hands over the colored zones and make downward motions to play!
Press 'Q' to quit
```

---

## ⌨️ Controls

- **Q** - Quit the application
- **ESC** - Alternative quit key

---

## 🎥 Visual Demo Description

Since I can't run it directly on your system, here's what you'll experience:

### Startup (0-2 seconds):
- Console shows startup messages
- Camera initializes
- Window opens with your webcam feed

### Playing (2+ seconds):
- You see yourself in the camera
- Three colored rectangular zones overlay the video:
  - **Top-left (RED)** - Hi-Hat zone
  - **Top-right (GREEN)** - Snare zone  
  - **Bottom (BLUE)** - Bass drum zone
- When you raise your hands:
  - Green lines connect your hand landmarks (skeleton)
  - Yellow circle (right hand) or magenta circle (left hand) follows your index finger
- When you make a quick downward motion over a zone:
  - Zone flashes brighter
  - Corresponding drum sound plays
  - Volume depends on how fast you moved

### Example Beat Pattern:
1. Move right hand over RED zone → Quick down → "Tss!" (Hi-hat)
2. Move left hand over GREEN zone → Quick down → "Crack!" (Snare)
3. Move both hands over BLUE zone → Quick down → "BOOM!" (Bass)
4. Repeat and create rhythms!

---

## 🔧 Troubleshooting

### "Python not found"
- Install Python from Microsoft Store or python.org
- Make sure to check "Add to PATH" during installation
- Restart your terminal after installation

### "No module named 'cv2'"
- Run: `python -m pip install opencv-python mediapipe pygame numpy scipy`

### "Camera not working"
- Close other apps using the camera (Zoom, Teams, etc.)
- Grant camera permissions in Windows Settings
- Try unplugging/replugging webcam

### "No sound files found"
- Run: `python setup_sounds.py`
- Check that `sounds/` folder exists with 3 WAV files

---

## 📞 Quick Setup Summary

**Complete setup in 5 minutes:**

1. **Install Python** (if needed)
   - Microsoft Store or python.org
   - Check "Add to PATH"

2. **Open PowerShell in project folder**
   - Right-click folder → "Open in Terminal"

3. **Run these commands:**
   ```powershell
   python -m pip install opencv-python mediapipe pygame numpy scipy
   python setup_sounds.py
   python air_drums.py
   ```

4. **Start playing!** 🥁

---

## 🎊 You're Ready!

Once Python is set up, you can run the application and start drumming!

**The experience is:**
- ✨ Smooth and responsive
- ✨ Fun and interactive
- ✨ Easy to learn
- ✨ Impressive to show friends!

---

**Need help? Check TROUBLESHOOTING.md for detailed solutions!**

*Happy Drumming! 🎵*
