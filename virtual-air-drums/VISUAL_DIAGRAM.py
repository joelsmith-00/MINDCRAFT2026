"""
Visual System Diagram - Virtual Air Drums
ASCII Art Representation
"""

SYSTEM_DIAGRAM = """
╔══════════════════════════════════════════════════════════════════════════╗
║                    VIRTUAL AIR DRUMS - SYSTEM FLOW                       ║
╚══════════════════════════════════════════════════════════════════════════╝


                            👋 USER HANDS 👋
                                   │
                                   │ Hand Movement
                                   ↓
                        ┌──────────────────────┐
                        │   📹 WEBCAM          │
                        │   Captures Video     │
                        │   30-60 FPS          │
                        └──────────────────────┘
                                   │
                                   │ Video Stream
                                   ↓
                        ┌──────────────────────┐
                        │   🎥 OpenCV          │
                        │   Frame Processing   │
                        │   RGB Conversion     │
                        └──────────────────────┘
                                   │
                                   │ Processed Frames
                                   ↓
                        ┌──────────────────────┐
                        │   ✋ MediaPipe        │
                        │   Hand Detection     │
                        │   21 Landmarks       │
                        └──────────────────────┘
                                   │
                                   │ Hand Coordinates
                                   ↓
                        ┌──────────────────────┐
                        │   🧠 Gesture Engine  │
                        │   Velocity Calc      │
                        │   Motion Detection   │
                        └──────────────────────┘
                                   │
                                   │ Gesture Data
                                   ↓
        ┌───────────────────────────────────────────────────┐
        │            🎯 DRUM ZONE DETECTION                 │
        │                                                   │
        │   ┌─────────────────┬─────────────────┐          │
        │   │  🔴 HI-HAT      │  🟢 SNARE       │          │
        │   │  (Top Left)     │  (Top Right)    │          │
        │   └─────────────────┴─────────────────┘          │
        │   ┌───────────────────────────────────┐          │
        │   │  🔵 BASS DRUM                     │          │
        │   │  (Bottom)                         │          │
        │   └───────────────────────────────────┘          │
        └───────────────────────────────────────────────────┘
                                   │
                                   │ Zone Hit Detected
                                   ↓
                        ┌──────────────────────┐
                        │   🎵 PyGame Audio    │
                        │   Sound Playback     │
                        │   Volume Control     │
                        └──────────────────────┘
                                   │
                                   │ Audio Output
                                   ↓
                        ┌──────────────────────┐
                        │   🔊 SPEAKERS        │
                        │   Drum Sounds        │
                        │   Real-time          │
                        └──────────────────────┘
                                   │
                                   │ Visual Feedback
                                   ↓
                        ┌──────────────────────┐
                        │   💻 DISPLAY         │
                        │   Zone Highlights    │
                        │   Hand Tracking      │
                        └──────────────────────┘
                                   │
                                   └─────────┐
                                             │
                                    ↻ LOOP REPEATS
                                    30-60 times/sec


╔══════════════════════════════════════════════════════════════════════════╗
║                         GESTURE RECOGNITION                              ║
╚══════════════════════════════════════════════════════════════════════════╝

    Hand Position (t₀)              Hand Position (t₁)
           ✋                               │
           │                                │
           │                                ↓
           │                                ✋
           │                                
           │← Calculate Velocity →          
           │   Speed = Distance/Time        
           │                                
           └─→ Downward Motion? ✓          
               Fast Enough? ✓              
               In Zone? ✓                  
               Cooldown OK? ✓              
                                            
               → TRIGGER HIT! 🥁           


╔══════════════════════════════════════════════════════════════════════════╗
║                          DRUM ZONE LAYOUT                                ║
╚══════════════════════════════════════════════════════════════════════════╝

    Screen View:
    
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃                                                                  ┃
    ┃  ┌─────────────────────────┬─────────────────────────┐         ┃
    ┃  │                         │                         │         ┃
    ┃  │      🔴 HI-HAT          │      🟢 SNARE           │         ┃
    ┃  │                         │                         │         ┃
    ┃  │    hihat.wav            │    snare.wav            │         ┃
    ┃  │                         │                         │         ┃
    ┃  └─────────────────────────┴─────────────────────────┘         ┃
    ┃  ┌───────────────────────────────────────────────────┐         ┃
    ┃  │                                                   │         ┃
    ┃  │              🔵 BASS DRUM                         │         ┃
    ┃  │                                                   │         ┃
    ┃  │              bass.wav                             │         ┃
    ┃  │                                                   │         ┃
    ┃  └───────────────────────────────────────────────────┘         ┃
    ┃                                                                  ┃
    ┃  FPS: 60  │  Instructions: Move hands to play!                  ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


╔══════════════════════════════════════════════════════════════════════════╗
║                        HAND TRACKING DETAIL                              ║
╚══════════════════════════════════════════════════════════════════════════╝

    MediaPipe Hand Landmarks (21 points):
    
           8 (Index Tip) ← WE TRACK THIS!
          /│\\
         / │ \\
        /  │  \\
       12  │  16  (Other fingers)
           │
           0 (Wrist)
    
    Tracking Data:
    • Position: (x, y) coordinates
    • Velocity: Speed of movement
    • Direction: Up/Down/Left/Right
    • History: Last 5 positions
    
    Hit Detection Logic:
    IF (velocity > 300 px/s) AND
       (moving downward) AND
       (inside drum zone) AND
       (cooldown elapsed)
    THEN
       → Play drum sound!
       → Volume = f(velocity)


╔══════════════════════════════════════════════════════════════════════════╗
║                         PERFORMANCE METRICS                              ║
╚══════════════════════════════════════════════════════════════════════════╝

    ⚡ Frame Rate:        30-60 FPS
    🎯 Detection Time:    ~16ms per frame
    🔊 Audio Latency:     <10ms
    ✋ Max Hands:         2 simultaneous
    📊 Accuracy:          70%+ confidence
    ⏱️  Cooldown:         0.3 seconds
    🎵 Sample Rate:       22050 Hz
    💾 Buffer Size:       512 samples


╔══════════════════════════════════════════════════════════════════════════╗
║                      TECHNOLOGY STACK                                    ║
╚══════════════════════════════════════════════════════════════════════════╝

    Layer               Technology          Purpose
    ─────────────────────────────────────────────────────────────
    Video Input         OpenCV 4.8.1        Camera capture
    Hand Detection      MediaPipe 0.10.9    Landmark detection
    Audio Output        PyGame 2.5.2        Sound playback
    Math Operations     NumPy 1.24.3        Calculations
    Sound Generation    SciPy (optional)    Synthesis
    Language            Python 3.8+         Core logic


╔══════════════════════════════════════════════════════════════════════════╗
║                         USER INTERACTION                                 ║
╚══════════════════════════════════════════════════════════════════════════╝

    1. User raises hands in front of camera
                    ↓
    2. System detects hand landmarks
                    ↓
    3. User makes quick downward motion
                    ↓
    4. System calculates velocity
                    ↓
    5. Checks if motion is in drum zone
                    ↓
    6. Plays corresponding drum sound
                    ↓
    7. Zone lights up (visual feedback)
                    ↓
    8. User hears sound and sees feedback
                    ↓
    9. Repeat for continuous drumming!


╔══════════════════════════════════════════════════════════════════════════╗
║                    COMPLETE SYSTEM OVERVIEW                              ║
╚══════════════════════════════════════════════════════════════════════════╝

    INPUT:  Hand movements in 3D space
            ↓
    CAPTURE: Webcam → 2D video frames
            ↓
    PROCESS: OpenCV → Image processing
            ↓
    DETECT: MediaPipe → Hand landmarks
            ↓
    ANALYZE: Custom logic → Gesture recognition
            ↓
    DECIDE: Zone detection → Which drum?
            ↓
    OUTPUT: PyGame → Audio playback
            ↓
    FEEDBACK: Visual → Zone highlights
            ↓
    LOOP: Repeat 30-60 times per second

    Result: Real-time, touch-free drumming experience! 🥁🎵
"""

if __name__ == "__main__":
    print(SYSTEM_DIAGRAM)
    print("\n" * 2)
    print("="*78)
    print("  Save this diagram for reference!")
    print("  Run: python air_drums.py to start playing!")
    print("="*78)
