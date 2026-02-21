"""
Visual Mockup - Virtual Air Drums Interface
ASCII Art representation of what you'll see when running
"""

INTERFACE_MOCKUP = """
╔══════════════════════════════════════════════════════════════════════════╗
║                   VIRTUAL AIR DRUMS - INTERFACE PREVIEW                  ║
╚══════════════════════════════════════════════════════════════════════════╝


┌────────────────────────────────────────────────────────────────────────┐
│ Virtual Air Drums                                              [-][□][X]│
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  FPS: 60                                                               │
│                                                                        │
│  ╔═══════════════════════════╦═══════════════════════════╗            │
│  ║                           ║                           ║            │
│  ║     🔴 HI-HAT             ║     🟢 SNARE              ║            │
│  ║                           ║                           ║            │
│  ║         ✋ ←──────────────║                           ║            │
│  ║        /│\\                ║                           ║            │
│  ║       / │ \\               ║                           ║            │
│  ║      /  │  \\              ║                           ║            │
│  ║     (Hand tracking)       ║                           ║            │
│  ║      ●←── Yellow circle   ║                           ║            │
│  ║      (Index finger)       ║                           ║            │
│  ║                           ║                           ║            │
│  ╚═══════════════════════════╩═══════════════════════════╝            │
│  ╔═══════════════════════════════════════════════════════╗            │
│  ║                                                       ║            │
│  ║              🔵 BASS DRUM                             ║            │
│  ║                                                       ║            │
│  ║                    ✋                                 ║            │
│  ║                   /│\\                                ║            │
│  ║                  / │ \\                               ║            │
│  ║                 (Hand tracking)                       ║            │
│  ║                  ●←── Magenta circle                  ║            │
│  ║                  (Index finger)                       ║            │
│  ║                                                       ║            │
│  ╚═══════════════════════════════════════════════════════╝            │
│                                                                        │
│  [Your webcam feed shows in the background]                           │
│                                                                        │
│  Virtual Air Drums - Move your hands to play!                         │
│  Fast downward motion = Hit                                            │
│  Speed = Volume                                                        │
│  Press 'Q' to quit                                                     │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════════╗
║                        WHAT YOU'LL SEE IN ACTION                         ║
╚══════════════════════════════════════════════════════════════════════════╝

BEFORE HIT:
┌─────────────────────┐
│   🔴 HI-HAT         │  ← Normal color (semi-transparent red)
│                     │
│        ✋           │  ← Your hand visible
│       /│\\          │
│      ●←─────────────┼─── Yellow circle on index finger
│                     │
└─────────────────────┘


DURING HIT (Quick downward motion):
┌─────────────────────┐
│   🔴 HI-HAT         │  ← Flashes BRIGHT RED!
│                     │
│                     │
│        ↓            │  ← Hand moving down
│        ✋           │
│       /│\\          │
│      ●             │
│                     │
└─────────────────────┘
        ↓
    🔊 "Tss!" sound plays


AFTER HIT:
┌─────────────────────┐
│   🔴 HI-HAT         │  ← Returns to normal color
│                     │
│        ✋           │  ← Hand can move away
│       /│\\          │
│      ●             │
│                     │
└─────────────────────┘


╔══════════════════════════════════════════════════════════════════════════╗
║                         HAND TRACKING DETAIL                             ║
╚══════════════════════════════════════════════════════════════════════════╝

What you see on your hands:

        8 ●←── Index finger tip (TRACKED!)
       /│\\
      / │ \\
     12 │ 16  ← Other finger tips
        │
     4 ●  ← Thumb tip
        │
        0  ← Wrist

Green lines connect all 21 landmarks
Yellow circle (right hand) or Magenta circle (left hand) on index finger


╔══════════════════════════════════════════════════════════════════════════╗
║                          PLAYING SEQUENCE                                ║
╚══════════════════════════════════════════════════════════════════════════╝

Step 1: RAISE HANDS
┌────────────────────────────────────┐
│                                    │
│         ✋          ✋              │
│        /│\\        /│\\             │
│       / │ \\      / │ \\            │
│        ●          ●               │
│   (Left hand) (Right hand)         │
│                                    │
│  Green skeleton appears!           │
│  Circles follow fingers!           │
└────────────────────────────────────┘


Step 2: POSITION OVER ZONE
┌─────────────────────┬─────────────────────┐
│   🔴 HI-HAT         │   🟢 SNARE          │
│                     │                     │
│        ✋           │         ✋          │
│       /│\\          │        /│\\         │
│        ●           │         ●          │
│   (Ready!)          │    (Ready!)         │
└─────────────────────┴─────────────────────┘


Step 3: QUICK DOWNWARD MOTION
┌─────────────────────┬─────────────────────┐
│   🔴 HI-HAT ✨      │   🟢 SNARE ✨       │
│   (FLASHING!)       │   (FLASHING!)       │
│                     │                     │
│        ↓            │         ↓           │
│        ✋           │         ✋          │
│        ●           │         ●          │
│                     │                     │
└─────────────────────┴─────────────────────┘
      🔊 "Tss!"            🔊 "Crack!"


Step 4: CREATE BEATS!
Pattern: Hi-Hat → Snare → Bass → Snare

🔴 "Tss!" → 🟢 "Crack!" → 🔵 "BOOM!" → 🟢 "Crack!"

Repeat and speed up for complex rhythms! 🎵


╔══════════════════════════════════════════════════════════════════════════╗
║                        VISUAL FEEDBACK SYSTEM                            ║
╚══════════════════════════════════════════════════════════════════════════╝

ZONE STATES:

1. IDLE (No hand nearby):
   ┌─────────────┐
   │  HI-HAT     │  ← Semi-transparent red
   │             │
   └─────────────┘

2. HAND DETECTED (Hand over zone, no hit):
   ┌─────────────┐
   │  HI-HAT     │  ← Same color
   │      ●      │  ← Circle visible
   └─────────────┘

3. HIT DETECTED (Quick downward motion):
   ┌─────────────┐
   │  HI-HAT ✨  │  ← BRIGHT flash!
   │             │  ← Zone lights up
   └─────────────┘
   🔊 Sound plays!

4. COOLDOWN (0.3 seconds after hit):
   ┌─────────────┐
   │  HI-HAT     │  ← Returns to normal
   │             │  ← Can't hit again yet
   └─────────────┘


╔══════════════════════════════════════════════════════════════════════════╗
║                      COMPLETE VISUAL EXPERIENCE                          ║
╚══════════════════════════════════════════════════════════════════════════╝

FULL WINDOW VIEW:

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Virtual Air Drums                                        [-][□][X] ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                     ┃
┃  FPS: 60  ←─── Performance indicator                               ┃
┃                                                                     ┃
┃  ┌─────────────────────────┬─────────────────────────┐            ┃
┃  │ 🔴 HI-HAT               │ 🟢 SNARE                │            ┃
┃  │                         │                         │            ┃
┃  │  [Webcam feed shows     │  your face and upper    │            ┃
┃  │   body in background]   │  body here]             │            ┃
┃  │                         │                         │            ┃
┃  │         ✋              │          ✋             │            ┃
┃  │        /│\\             │         /│\\            │            ┃
┃  │       ●─┼─●            │        ●─┼─●           │            ┃
┃  │    (Hand skeleton)      │    (Hand skeleton)      │            ┃
┃  │                         │                         │            ┃
┃  └─────────────────────────┴─────────────────────────┘            ┃
┃  ┌───────────────────────────────────────────────────┐            ┃
┃  │ 🔵 BASS DRUM                                      │            ┃
┃  │                                                   │            ┃
┃  │  [Webcam feed continues showing your lower body]  │            ┃
┃  │                                                   │            ┃
┃  │                    ✋                             │            ┃
┃  │                   /│\\                            │            ┃
┃  │                  ●─┼─●                           │            ┃
┃  │              (Hand skeleton)                      │            ┃
┃  │                                                   │            ┃
┃  └───────────────────────────────────────────────────┘            ┃
┃                                                                     ┃
┃  Virtual Air Drums - Move your hands to play! ←─ Instructions     ┃
┃  Fast downward motion = Hit                                        ┃
┃  Speed = Volume                                                    ┃
┃  Press 'Q' to quit                                                 ┃
┃                                                                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


COLORS YOU'LL SEE:
• 🔴 Red zone (Hi-Hat) - Top left
• 🟢 Green zone (Snare) - Top right  
• 🔵 Blue zone (Bass) - Bottom
• Green lines - Hand skeleton
• Yellow circle - Right hand index finger
• Magenta circle - Left hand index finger
• White text - Instructions and labels


ANIMATIONS:
• Zones pulse brighter when hit (0.2 second flash)
• Hand skeleton follows your movements smoothly
• Colored circles track finger tips in real-time
• FPS counter updates continuously
• Smooth 30-60 FPS video feed


SOUNDS:
• 🔴 Hi-Hat: "Tss tss" (high pitched)
• 🟢 Snare: "Crack!" (sharp snap)
• 🔵 Bass: "BOOM!" (deep thump)
• Volume varies with hit speed
• Instant playback (<10ms latency)
"""

def show_mockup():
    """Display the interface mockup"""
    print(INTERFACE_MOCKUP)
    print("\n" * 2)
    print("="*78)
    print("  To see this in action, run: python air_drums.py")
    print("  Make sure to install dependencies first!")
    print("="*78)

if __name__ == "__main__":
    show_mockup()
