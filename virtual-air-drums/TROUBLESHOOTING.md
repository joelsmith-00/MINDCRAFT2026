# 🔧 Troubleshooting Guide - Virtual Air Drums

## Common Issues and Solutions

### 🎥 Camera Issues

#### Camera Not Detected
**Problem:** "Failed to capture frame" or black screen

**Solutions:**
1. Check if camera is connected and working
   - Test camera in other apps (Zoom, Skype, etc.)
   - Try a different USB port
   
2. Change camera index in code
   - Edit `air_drums.py` line 88
   - Try: `cv2.VideoCapture(1)` or `cv2.VideoCapture(2)`
   
3. Grant camera permissions
   - Windows: Settings → Privacy → Camera
   - macOS: System Preferences → Security & Privacy → Camera
   
4. Close other apps using camera
   - Zoom, Teams, Skype, etc.
   - Only one app can use camera at a time

#### Poor Camera Quality
**Problem:** Blurry or low-quality video

**Solutions:**
1. Clean camera lens
2. Improve lighting in room
3. Adjust camera resolution in `config.py`
4. Update camera drivers

---

### ✋ Hand Detection Issues

#### Hands Not Detected
**Problem:** System doesn't see your hands

**Solutions:**
1. **Improve Lighting**
   - Use bright, even lighting
   - Avoid backlighting (light behind you)
   - Natural daylight works best
   
2. **Adjust Position**
   - Sit 2-3 feet from camera
   - Keep hands in camera view
   - Ensure full hand is visible
   
3. **Simplify Background**
   - Use plain background
   - Avoid cluttered areas
   - Remove objects that look like hands
   
4. **Lower Detection Confidence**
   - Edit `config.py`
   - Set `DETECTION_CONFIDENCE = 0.5`
   
5. **Check Hand Visibility**
   - Wear contrasting clothing
   - Avoid gloves or hand coverings
   - Ensure good skin tone contrast

#### Hands Detected Incorrectly
**Problem:** False detections or wrong hand tracking

**Solutions:**
1. Remove objects from view
2. Increase `DETECTION_CONFIDENCE` to 0.8
3. Use better lighting
4. Keep background simple

---

### 🥁 Drum Hit Detection Issues

#### Hits Not Registering
**Problem:** Moving hands but no sound plays

**Solutions:**
1. **Move Faster**
   - Make quick, deliberate downward motions
   - Slow movements won't trigger
   - Think "drum stick hitting drum"
   
2. **Lower Velocity Threshold**
   - Edit `config.py`
   - Set `VELOCITY_THRESHOLD = 200`
   - Lower = easier to trigger
   
3. **Check Zone Position**
   - Ensure finger is inside colored zone
   - Watch the finger indicator circle
   - Zones are clearly marked
   
4. **Verify Downward Motion**
   - Must move DOWN (not sideways)
   - Quick vertical motion works best

#### Too Many False Hits
**Problem:** Sounds playing when you don't want them

**Solutions:**
1. **Increase Velocity Threshold**
   - Edit `config.py`
   - Set `VELOCITY_THRESHOLD = 500`
   - Higher = need faster movements
   
2. **Increase Cooldown**
   - Edit `config.py`
   - Set `HIT_COOLDOWN = 0.5`
   - Prevents rapid double-hits
   
3. **Make More Deliberate Movements**
   - Avoid hovering over zones
   - Clear "hit and retreat" motions

---

### 🔊 Audio Issues

#### No Sound Playing
**Problem:** Hits register but no audio

**Solutions:**
1. **Check Sound Files**
   ```bash
   # Verify files exist
   dir sounds
   # Should show: hihat.wav, snare.wav, bass.wav
   ```
   
2. **Verify File Format**
   - Must be WAV format
   - Convert MP3/OGG to WAV if needed
   - Use online converters or Audacity
   
3. **Check File Names**
   - Must be exactly: `hihat.wav`, `snare.wav`, `bass.wav`
   - Case-sensitive on some systems
   - No extra spaces
   
4. **Check System Volume**
   - Turn up speaker volume
   - Unmute system audio
   - Check app isn't muted
   
5. **Regenerate Sounds**
   ```bash
   python setup_sounds.py
   ```

#### Audio Crackling/Glitching
**Problem:** Sound quality is poor

**Solutions:**
1. **Increase Audio Buffer**
   - Edit `config.py`
   - Set `AUDIO_BUFFER_SIZE = 1024`
   
2. **Use Better Sound Files**
   - Download professional samples
   - Ensure proper WAV format
   
3. **Close Other Audio Apps**
   - Stop music players
   - Close video calls
   
4. **Update Audio Drivers**

#### Audio Delay/Latency
**Problem:** Sound plays late after hit

**Solutions:**
1. **Decrease Audio Buffer**
   - Edit `config.py`
   - Set `AUDIO_BUFFER_SIZE = 256`
   - Warning: May cause glitches
   
2. **Close Background Apps**
   - Free up system resources
   
3. **Use Wired Headphones**
   - Bluetooth adds latency

---

### 💻 Performance Issues

#### Low FPS / Lag
**Problem:** System runs slowly

**Solutions:**
1. **Lower Camera Resolution**
   - Edit `config.py`
   - Set `FRAME_WIDTH = 640`
   - Set `FRAME_HEIGHT = 480`
   
2. **Reduce Max Hands**
   - Edit `config.py`
   - Set `MAX_HANDS = 1`
   
3. **Close Other Apps**
   - Free up CPU and RAM
   - Close browser tabs
   
4. **Update Graphics Drivers**
   
5. **Use More Powerful Computer**
   - Minimum: Intel i3, 4GB RAM
   - Recommended: Intel i5+, 8GB RAM

#### High CPU Usage
**Problem:** Computer gets hot/loud

**Solutions:**
1. Lower resolution (see above)
2. Reduce target FPS in code
3. Close background apps
4. Improve cooling

---

### 🐍 Python/Package Issues

#### "Module not found" Error
**Problem:** `ImportError: No module named 'cv2'` (or similar)

**Solutions:**
```bash
# Install missing package
python -m pip install opencv-python
python -m pip install mediapipe
python -m pip install pygame
python -m pip install numpy
```

#### "Python not found" Error
**Problem:** `'python' is not recognized...`

**Solutions:**
1. Install Python from python.org
2. Check "Add to PATH" during installation
3. Try `python3` instead of `python`
4. Try `py` instead of `python` (Windows)

#### Package Installation Fails
**Problem:** pip install errors

**Solutions:**
```bash
# Update pip
python -m pip install --upgrade pip

# Install with verbose output
python -m pip install opencv-python --verbose

# Try different package versions
python -m pip install opencv-python==4.8.0.76
```

---

### 🎨 Visual Issues

#### Zones Not Visible
**Problem:** Can't see colored drum zones

**Solutions:**
1. Check `ZONE_TRANSPARENCY` in `config.py`
2. Adjust zone colors for better visibility
3. Ensure good monitor brightness

#### Hand Landmarks Not Showing
**Problem:** Don't see hand skeleton

**Solutions:**
1. Set `SHOW_HAND_LANDMARKS = True` in `config.py`
2. Ensure hands are detected (check console)

---

## 🆘 Still Having Issues?

### Diagnostic Steps

1. **Run System Architecture Viewer**
   ```bash
   python system_architecture.py
   ```
   This shows how the system works

2. **Enable Debug Mode**
   - Edit `config.py`
   - Set `DEBUG_MODE = True`
   - Set `LOG_HITS = True`
   - Check console for error messages

3. **Test Individual Components**
   ```python
   # Test camera
   import cv2
   cap = cv2.VideoCapture(0)
   ret, frame = cap.read()
   print("Camera working:", ret)
   
   # Test audio
   import pygame
   pygame.mixer.init()
   print("Audio working: OK")
   
   # Test hand detection
   import mediapipe as mp
   print("MediaPipe working: OK")
   ```

4. **Check System Requirements**
   - Python 3.8+
   - 4GB+ RAM
   - Working webcam
   - Working audio output

### Getting Help

If you're still stuck:
1. Check the README.md for more info
2. Review the INSTALL.md guide
3. Make sure all dependencies are installed
4. Try on a different computer
5. Check if your webcam works in other apps

---

## 📋 Quick Checklist

Before asking for help, verify:
- [ ] Python 3.8+ installed
- [ ] All packages installed (`pip list`)
- [ ] Camera working in other apps
- [ ] Sound files exist in `sounds/` folder
- [ ] File names are correct
- [ ] Good lighting on hands
- [ ] Hands visible to camera
- [ ] System volume turned up
- [ ] No other apps using camera
- [ ] Tried restarting the application
- [ ] Tried restarting the computer

---

**Most issues are solved by:**
1. Better lighting
2. Faster hand movements  
3. Correct sound file setup
4. Proper Python installation

Good luck and happy drumming! 🥁🎵
