"""
Virtual Air Drums System
A touch-free drumming system using hand gesture recognition
"""

import cv2
import mediapipe as mp
import pygame
import numpy as np
import time
from collections import deque

# Initialize Pygame for sound
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Initialize MediaPipe Hand Detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

class DrumZone:
    """Represents a virtual drum zone on the screen"""
    def __init__(self, name, x1, y1, x2, y2, sound_file, color):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.sound = pygame.mixer.Sound(sound_file)
        self.color = color
        self.active_color = tuple(min(c + 100, 255) for c in color)
        self.is_hit = False
        self.hit_time = 0
        
    def contains_point(self, x, y):
        """Check if a point is inside this drum zone"""
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2
    
    def play(self, volume=1.0):
        """Play the drum sound with specified volume"""
        self.sound.set_volume(min(volume, 1.0))
        self.sound.play()
        self.is_hit = True
        self.hit_time = time.time()
    
    def draw(self, frame):
        """Draw the drum zone on the frame"""
        current_time = time.time()
        # Show active color for 0.2 seconds after hit
        if self.is_hit and (current_time - self.hit_time) < 0.2:
            color = self.active_color
        else:
            color = self.color
            self.is_hit = False
        
        # Draw semi-transparent rectangle
        overlay = frame.copy()
        cv2.rectangle(overlay, (self.x1, self.y1), (self.x2, self.y2), color, -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        # Draw border
        cv2.rectangle(frame, (self.x1, self.y1), (self.x2, self.y2), color, 3)
        
        # Draw label
        label_y = self.y1 + 30
        cv2.putText(frame, self.name, (self.x1 + 10, label_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

class HandTracker:
    """Tracks hand movements and detects drum hits"""
    def __init__(self):
        self.position_history = deque(maxlen=5)  # Track last 5 positions
        self.last_hit_time = 0
        self.hit_cooldown = 0.3  # Minimum time between hits (seconds)
        
    def update(self, x, y):
        """Update hand position"""
        self.position_history.append((x, y, time.time()))
    
    def get_velocity(self):
        """Calculate hand movement velocity"""
        if len(self.position_history) < 2:
            return 0
        
        # Calculate velocity based on recent positions
        recent = list(self.position_history)[-2:]
        dx = recent[1][0] - recent[0][0]
        dy = recent[1][1] - recent[0][1]
        dt = recent[1][2] - recent[0][2]
        
        if dt == 0:
            return 0
        
        # Calculate speed (pixels per second)
        speed = np.sqrt(dx**2 + dy**2) / dt
        return speed
    
    def is_downward_motion(self):
        """Check if hand is moving downward"""
        if len(self.position_history) < 2:
            return False
        
        recent = list(self.position_history)[-2:]
        dy = recent[1][1] - recent[0][1]
        return dy > 5  # Moving down
    
    def can_hit(self):
        """Check if enough time has passed since last hit"""
        return (time.time() - self.last_hit_time) > self.hit_cooldown
    
    def register_hit(self):
        """Register that a hit occurred"""
        self.last_hit_time = time.time()

class VirtualAirDrums:
    """Main application class"""
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Get actual frame dimensions
        ret, frame = self.cap.read()
        if ret:
            self.height, self.width = frame.shape[:2]
        else:
            self.width, self.height = 1280, 720
        
        # Initialize drum zones
        self.setup_drum_zones()
        
        # Hand trackers for left and right hands
        self.left_hand_tracker = HandTracker()
        self.right_hand_tracker = HandTracker()
        
        # Performance metrics
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        
    def setup_drum_zones(self):
        """Create virtual drum zones"""
        zone_height = self.height // 2
        zone_width = self.width // 2
        
        # Create drum zones with different sounds
        self.drum_zones = [
            # Top row
            DrumZone("HI-HAT", 0, 0, zone_width, zone_height,
                    "sounds/hihat.wav", (255, 100, 100)),  # Red
            DrumZone("SNARE", zone_width, 0, self.width, zone_height,
                    "sounds/snare.wav", (100, 255, 100)),  # Green
            # Bottom row
            DrumZone("BASS DRUM", 0, zone_height, self.width, self.height,
                    "sounds/bass.wav", (100, 100, 255)),  # Blue
        ]
    
    def process_hand(self, hand_landmarks, handedness, frame):
        """Process individual hand and check for drum hits"""
        # Get index finger tip position (landmark 8)
        index_tip = hand_landmarks.landmark[8]
        x = int(index_tip.x * self.width)
        y = int(index_tip.y * self.height)
        
        # Determine which hand
        is_right_hand = handedness.classification[0].label == "Right"
        tracker = self.right_hand_tracker if is_right_hand else self.left_hand_tracker
        
        # Update tracker
        tracker.update(x, y)
        
        # Draw hand landmarks
        mp_drawing.draw_landmarks(
            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2)
        )
        
        # Draw finger tip indicator
        color = (0, 255, 255) if is_right_hand else (255, 0, 255)
        cv2.circle(frame, (x, y), 15, color, -1)
        cv2.circle(frame, (x, y), 20, (255, 255, 255), 2)
        
        # Check for drum hit
        if tracker.is_downward_motion() and tracker.can_hit():
            velocity = tracker.get_velocity()
            
            # Velocity threshold for hit detection
            if velocity > 300:  # Adjust this threshold as needed
                # Check which drum zone was hit
                for zone in self.drum_zones:
                    if zone.contains_point(x, y):
                        # Calculate volume based on velocity (faster = louder)
                        volume = min(velocity / 2000, 1.0)
                        zone.play(volume)
                        tracker.register_hit()
                        break
    
    def draw_ui(self, frame):
        """Draw UI elements"""
        # Draw FPS
        cv2.putText(frame, f"FPS: {self.fps:.1f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw instructions
        instructions = [
            "Virtual Air Drums - Move your hands to play!",
            "Fast downward motion = Hit",
            "Speed = Volume",
            "Press 'Q' to quit"
        ]
        
        y_offset = self.height - 120
        for i, text in enumerate(instructions):
            cv2.putText(frame, text, (10, y_offset + i * 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    def run(self):
        """Main application loop"""
        print("🥁 Virtual Air Drums System Starting...")
        print("📹 Camera initialized")
        print("🎵 Drum zones created")
        print("✋ Hand detection ready")
        print("\nMove your hands over the colored zones and make downward motions to play!")
        print("Press 'Q' to quit\n")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame with MediaPipe
            results = hands.process(rgb_frame)
            
            # Draw drum zones
            for zone in self.drum_zones:
                zone.draw(frame)
            
            # Process detected hands
            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, 
                                                      results.multi_handedness):
                    self.process_hand(hand_landmarks, handedness, frame)
            
            # Draw UI
            self.draw_ui(frame)
            
            # Calculate FPS
            self.frame_count += 1
            if self.frame_count % 10 == 0:
                elapsed = time.time() - self.start_time
                self.fps = self.frame_count / elapsed
            
            # Display frame
            cv2.imshow('Virtual Air Drums', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        hands.close()
        pygame.mixer.quit()
        print("\n👋 Thanks for playing!")

if __name__ == "__main__":
    try:
        app = VirtualAirDrums()
        app.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have:")
        print("  1. A working webcam")
        print("  2. Sound files in the 'sounds' folder")
        print("  3. All required packages installed")
