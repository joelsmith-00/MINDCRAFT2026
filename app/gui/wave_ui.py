import sys
import math
import time
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QLinearGradient

# --- Colors (Mindcraft Palette) ---
PALETTE = ["#1b120e", "#34251b", "#534030", "#7b5f48", "#a68569"]
BG_COLOR = QColor("#1b120e")

# --- Layer Configs ---
LAYERS = [
    {"p0": 0, "p1": 1, "p2": 2, "baseAmp": 0.10, "voiceAmp": 0.68, "speed": 0.00110, "freq": 2.0},
    {"p0": 1, "p1": 2, "p2": 3, "baseAmp": 0.08, "voiceAmp": 0.58, "speed": 0.00140, "freq": 2.5},
    {"p0": 2, "p1": 3, "p2": 4, "baseAmp": 0.06, "voiceAmp": 0.46, "speed": 0.00170, "freq": 3.1},
    {"p0": 1, "p1": 3, "p2": 4, "baseAmp": 0.04, "voiceAmp": 0.34, "speed": 0.00210, "freq": 3.8},
]

class WaveVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_paused = False
        self.smooth_energy = 0.0
        self.last_ts = time.time() * 1000
        self.phases = [0.0] * len(LAYERS)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16) # ~60 FPS

    def animate(self):
        if self.is_paused:
            return
            
        current_ts = time.time() * 1000
        dt = min(current_ts - self.last_ts, 50)
        self.last_ts = current_ts

        # Pulse simulation (No mic access to avoid conflicts with speech recognition)
        target_energy = 0.15 + (math.sin(current_ts * 0.002) + 1) * 0.1
        self.smooth_energy += (target_energy - self.smooth_energy) * 0.1

        for i in range(len(LAYERS)):
            self.phases[i] += LAYERS[i]["speed"] * (1 + self.smooth_energy * 2.2) * dt
            
        self.update()

    def set_paused(self, paused):
        self.is_paused = paused
        self.update()

    def hex_to_rgb(self, hex_str):
        hex_str = hex_str.lstrip('#')
        return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

    def lerp_color(self, hex1, hex2, t, alpha):
        r1, g1, b1 = self.hex_to_rgb(hex1)
        r2, g2, b2 = self.hex_to_rgb(hex2)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return QColor(r, g, b, int(alpha * 255))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        W = self.width()
        H = self.height()
        painter.fillRect(self.rect(), BG_COLOR)

        if self.is_paused:
            painter.setPen(QColor("#7b5f48"))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "PAUSED")
            return

        for i, layer in enumerate(LAYERS):
            self.draw_wave_layer(painter, i, layer, W, H)

    def draw_wave_layer(self, painter, idx, layer, W, H):
        amp_val = layer["baseAmp"] + self.smooth_energy * layer["voiceAmp"]
        ph = self.phases[idx]
        num_pts = 100
        
        path = QPainterPath()
        path.moveTo(0, H)
        
        points = []
        for i in range(num_pts + 1):
            t = i / num_pts
            x = t * W
            w1 = math.sin(2 * math.pi * layer["freq"] * t + ph)
            w2 = 0.42 * math.sin(2 * math.pi * layer["freq"] * 1.73 * t + ph * 1.4 + 1.1)
            w3 = 0.20 * math.sin(2 * math.pi * layer["freq"] * 0.47 * t + ph * 0.6 + 2.8)
            wave_y = (w1 + w2 + w3) / (1 + 0.42 + 0.20)
            y = H * 0.97 - (wave_y * 0.5 + 0.5) * amp_val * H
            points.append(QPointF(x, y))

        path.lineTo(points[0])
        for i in range(len(points) - 1):
            pt1 = points[i]
            pt2 = points[i+1]
            mid = (pt1 + pt2) / 2
            path.quadTo(pt1, mid)
        
        path.lineTo(W, points[-1].y())
        path.lineTo(W, H)
        path.closeSubpath()

        edge = self.lerp_color(PALETTE[layer["p0"]], PALETTE[layer["p1"]], 0.2, 0.96)
        mid = self.lerp_color(PALETTE[layer["p1"]], PALETTE[layer["p2"]], 0.3, 0.90)
        crest = self.lerp_color(PALETTE[layer["p1"]], PALETTE[layer["p2"]], 0.4 + self.smooth_energy * 0.6, 0.85)

        grad = QLinearGradient(0, 0, W, 0)
        grad.setColorAt(0.00, edge)
        grad.setColorAt(0.25, mid)
        grad.setColorAt(0.50, crest)
        grad.setColorAt(0.75, mid)
        grad.setColorAt(1.00, edge)

        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)

class MindcraftGUI(QMainWindow):
    def __init__(self, pause_event):
        super().__init__()
        self.pause_event = pause_event
        self.is_paused = False
        
        self.setWindowTitle("LUMI - Mindcraft Interface")
        self.resize(1000, 400)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.visualizer = WaveVisualizer()
        self.setCentralWidget(self.visualizer)

    def mousePressEvent(self, event):
        self.toggle_pause()
        
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.visualizer.set_paused(self.is_paused)
        if self.is_paused:
            self.pause_event.set()
        else:
            self.pause_event.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

def run_gui(pause_event):
    app = QApplication(sys.argv)
    window = MindcraftGUI(pause_event)
    window.show()
    sys.exit(app.exec())
