"""
System Architecture and Flow Visualization
Virtual Air Drums System
"""

def print_system_overview():
    """Print detailed system architecture"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                    VIRTUAL AIR DRUMS SYSTEM                              ║
║                         System Architecture                              ║
╚══════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────┐
│                          HARDWARE LAYER                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  📹 Webcam  →  Captures hand movements at 30-60 FPS                     │
│  🔊 Speakers → Plays drum sounds in real-time                           │
│  💻 Computer → Processes video and audio                                │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                       VIDEO CAPTURE MODULE                               │
├─────────────────────────────────────────────────────────────────────────┤
│  • OpenCV captures video frames                                         │
│  • Frame rate: 30-60 FPS                                                │
│  • Resolution: 1280x720 (adjustable)                                    │
│  • Mirror mode: Enabled for natural interaction                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                      FRAME PREPROCESSING                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  • Convert BGR → RGB (MediaPipe requirement)                            │
│  • Flip horizontally (mirror effect)                                    │
│  • Optimize for hand detection                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                      HAND DETECTION (MediaPipe)                          │
├─────────────────────────────────────────────────────────────────────────┤
│  • Detects up to 2 hands simultaneously                                 │
│  • Identifies 21 landmarks per hand                                     │
│  • Tracks finger positions (x, y coordinates)                           │
│  • Distinguishes left vs right hand                                     │
│  • Confidence threshold: 70%                                            │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                      GESTURE RECOGNITION ENGINE                          │
├─────────────────────────────────────────────────────────────────────────┤
│  📍 Position Tracking:                                                   │
│     • Tracks index finger tip (landmark #8)                             │
│     • Stores last 5 positions in history buffer                         │
│     • Calculates real-time position changes                             │
│                                                                          │
│  ⚡ Velocity Calculation:                                                │
│     • Speed = √(dx² + dy²) / dt                                         │
│     • Measured in pixels per second                                     │
│     • Threshold: 300 px/s for hit detection                             │
│                                                                          │
│  ⬇️  Motion Detection:                                                   │
│     • Detects downward motion (dy > 5 pixels)                           │
│     • Filters out slow movements                                        │
│     • Prevents false triggers                                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                        DRUM ZONE DETECTION                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────────────────┬─────────────────────┐                        │
│   │     HI-HAT (Red)    │    SNARE (Green)    │                        │
│   │   Zone: Top-Left    │   Zone: Top-Right   │                        │
│   │   Sound: hihat.wav  │   Sound: snare.wav  │                        │
│   └─────────────────────┴─────────────────────┘                        │
│   ┌───────────────────────────────────────────┐                        │
│   │          BASS DRUM (Blue)                 │                        │
│   │          Zone: Bottom                     │                        │
│   │          Sound: bass.wav                  │                        │
│   └───────────────────────────────────────────┘                        │
│                                                                          │
│  • Checks if finger position is inside zone                             │
│  • Each zone mapped to specific sound file                              │
│  • Visual feedback on hit                                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                         HIT VALIDATION                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  ✓ Downward motion detected?                                            │
│  ✓ Velocity > threshold (300 px/s)?                                     │
│  ✓ Finger inside drum zone?                                             │
│  ✓ Cooldown period elapsed (0.3s)?                                      │
│                                                                          │
│  If ALL conditions met → TRIGGER DRUM HIT                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                        AUDIO PLAYBACK (PyGame)                           │
├─────────────────────────────────────────────────────────────────────────┤
│  🎵 Sound Processing:                                                    │
│     • Load WAV file from memory                                         │
│     • Calculate volume: min(velocity/2000, 1.0)                         │
│     • Fast hit = Loud sound                                             │
│     • Slow hit = Soft sound                                             │
│                                                                          │
│  🔊 Playback:                                                            │
│     • Low latency audio buffer (512 samples)                            │
│     • Instant sound trigger (<10ms delay)                               │
│     • Multiple sounds can overlap                                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                        VISUAL FEEDBACK                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  • Drum zones light up on hit (0.2s duration)                           │
│  • Hand landmarks drawn in real-time                                    │
│  • Finger tip highlighted with colored circle                           │
│  • FPS counter displayed                                                │
│  • Instructions overlay                                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                      CONTINUOUS LOOP (30-60 Hz)                          │
├─────────────────────────────────────────────────────────────────────────┤
│  while True:                                                             │
│      1. Capture frame                                                   │
│      2. Detect hands                                                    │
│      3. Track movements                                                 │
│      4. Recognize gestures                                              │
│      5. Play sounds                                                     │
│      6. Update display                                                  │
│      7. Check for quit (Q key)                                          │
│      8. Repeat                                                          │
└─────────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════════╗
║                           KEY FEATURES                                   ║
╠══════════════════════════════════════════════════════════════════════════╣
║  ✅ Real-time processing (30-60 FPS)                                     ║
║  ✅ Multi-hand support (up to 2 hands)                                   ║
║  ✅ Dynamic volume control (velocity-based)                              ║
║  ✅ Visual feedback (zone highlighting)                                  ║
║  ✅ Low latency audio (<10ms)                                            ║
║  ✅ Cooldown system (prevents double-hits)                               ║
║  ✅ Touch-free interaction                                               ║
╚══════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════╗
║                        TECHNICAL SPECIFICATIONS                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║  Video Processing:    OpenCV 4.8.1                                       ║
║  Hand Detection:      MediaPipe 0.10.9                                   ║
║  Audio Engine:        PyGame 2.5.2                                       ║
║  Numerical Ops:       NumPy 1.24.3                                       ║
║  Frame Rate:          30-60 FPS                                          ║
║  Audio Sample Rate:   22050 Hz                                           ║
║  Audio Buffer:        512 samples                                        ║
║  Detection Conf:      70%                                                ║
║  Tracking Conf:       50%                                                ║
║  Hit Threshold:       300 px/s                                           ║
║  Cooldown Period:     0.3 seconds                                        ║
╚══════════════════════════════════════════════════════════════════════════╝
""")

def print_data_flow():
    """Print data flow diagram"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                          DATA FLOW DIAGRAM                               ║
╚══════════════════════════════════════════════════════════════════════════╝

User Hand Movement
        │
        ├─→ Camera captures at 30-60 FPS
        │
        ├─→ Frame (1280x720 pixels)
        │
        ├─→ RGB Conversion
        │
        ├─→ MediaPipe Hand Detection
        │       │
        │       ├─→ Hand Landmarks (21 points × 2 hands)
        │       │       │
        │       │       ├─→ Index Finger Tip (x, y)
        │       │       │
        │       │       └─→ Position History Buffer [5 positions]
        │       │
        │       └─→ Handedness (Left/Right)
        │
        ├─→ Velocity Calculation
        │       │
        │       └─→ Speed (pixels/second)
        │
        ├─→ Motion Analysis
        │       │
        │       ├─→ Direction (up/down)
        │       └─→ Threshold Check (>300 px/s)
        │
        ├─→ Zone Detection
        │       │
        │       ├─→ Hi-Hat Zone? → hihat.wav
        │       ├─→ Snare Zone?  → snare.wav
        │       └─→ Bass Zone?   → bass.wav
        │
        ├─→ Hit Validation
        │       │
        │       ├─→ Downward? ✓
        │       ├─→ Fast enough? ✓
        │       ├─→ In zone? ✓
        │       └─→ Cooldown OK? ✓
        │
        ├─→ Volume Calculation
        │       │
        │       └─→ Volume = min(velocity/2000, 1.0)
        │
        ├─→ Audio Playback
        │       │
        │       └─→ 🔊 Sound Output
        │
        └─→ Visual Feedback
                │
                ├─→ Zone Highlight
                ├─→ Hand Skeleton
                └─→ Finger Indicator

Loop repeats 30-60 times per second ↻
""")

def print_gesture_recognition():
    """Print gesture recognition logic"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                      GESTURE RECOGNITION LOGIC                           ║
╚══════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 1: Position Tracking                                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Current Position: (x₁, y₁, t₁)                                         │
│  Previous Position: (x₀, y₀, t₀)                                        │
│                                                                          │
│  History Buffer: [(x₋₄,y₋₄,t₋₄), ..., (x₀,y₀,t₀), (x₁,y₁,t₁)]        │
│                   └────────── Last 5 positions ──────────┘              │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 2: Velocity Calculation                                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Δx = x₁ - x₀                                                           │
│  Δy = y₁ - y₀                                                           │
│  Δt = t₁ - t₀                                                           │
│                                                                          │
│  Distance = √(Δx² + Δy²)                                                │
│  Velocity = Distance / Δt                                               │
│                                                                          │
│  Example:                                                               │
│    Δx = 50 pixels, Δy = 100 pixels, Δt = 0.033s (30 FPS)               │
│    Distance = √(50² + 100²) = 111.8 pixels                             │
│    Velocity = 111.8 / 0.033 = 3,388 px/s ✓ (Hit!)                      │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 3: Motion Direction                                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  if Δy > 5:                                                             │
│      → Downward motion ✓                                                │
│  else:                                                                  │
│      → Not a hit ✗                                                      │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 4: Threshold Check                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  if Velocity > 300 px/s:                                                │
│      → Fast enough ✓                                                    │
│  else:                                                                  │
│      → Too slow ✗                                                       │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 5: Cooldown Check                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Time since last hit = Current Time - Last Hit Time                     │
│                                                                          │
│  if Time since last hit > 0.3s:                                         │
│      → Cooldown OK ✓                                                    │
│  else:                                                                  │
│      → Too soon, ignore ✗                                               │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ STEP 6: Final Decision                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  if (Downward ✓) AND (Fast ✓) AND (In Zone ✓) AND (Cooldown ✓):       │
│      → TRIGGER DRUM HIT! 🥁                                             │
│      → Calculate Volume = min(Velocity/2000, 1.0)                       │
│      → Play Sound                                                       │
│      → Update Last Hit Time                                             │
│  else:                                                                  │
│      → No hit, continue tracking                                        │
└─────────────────────────────────────────────────────────────────────────┘
""")

if __name__ == "__main__":
    print_system_overview()
    print("\n" * 2)
    print_data_flow()
    print("\n" * 2)
    print_gesture_recognition()
    
    print("\n" * 2)
    print("="*78)
    print("  📚 For more information, see README.md and QUICKSTART.md")
    print("  🚀 To run the system: python air_drums.py")
    print("="*78)
