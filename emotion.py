"""
Real-Time Emotion Detection System
====================================
Stack : OpenCV · YOLOv8 (ultralytics) · DeepFace
Author: AI Assistant  |  Suitable for AI-assistant integration

Architecture
------------
  1. YOLOv8  → detect person bounding boxes (class 0 = person)
  2. Haar Cascade (within person crop) → isolate the face precisely
  3. DeepFace  → emotion + age + gender (every FRAME_SKIP frames)
  4. Centroid Tracker → stable per-face IDs across frames
  5. Confidence filter + ambiguity check → reject noisy predictions
  6. Rolling majority vote + emotion lock → prevent flickering
  7. Rich OpenCV overlay → coloured box, confidence bars, FPS
"""

import cv2
import time
import numpy as np
from deepface import DeepFace
from collections import Counter, deque
from ultralytics import YOLO

# ══════════════════════════════════════════════════════════════════
# TUNABLE CONFIGURATION
# ══════════════════════════════════════════════════════════════════
FRAME_SKIP       = 6     # Run DeepFace every N frames (higher = faster, less responsive)
SMOOTHING_WINDOW = 15    # Rolling history length per face
CONF_THRESHOLD   = 45.0  # Min % for dominant emotion to be accepted
AMBIGUITY_MARGIN = 18.0  # If (top1 - top2) < this → too ambiguous → use "neutral"
LOCK_FRAMES      = 4     # Stable frames needed before emotion label switches
MAX_DISAPPEARED  = 25    # Frames a face can vanish before its ID is purged
TRACK_DIST_MAX   = 120   # Max centroid shift (px) to match same face ID

# BGR colour palette — one colour per emotion
EMOTION_COLORS = {
    "happy":    (0,   215, 255),
    "sad":      (210,  80,  30),
    "angry":    (0,    0,  230),
    "surprise": (0,   200, 200),
    "fear":     (160,  40, 200),
    "disgust":  (30,  160,  30),
    "neutral":  (170, 170, 170),
}
DEFAULT_COLOR = (0, 200, 0)


# ══════════════════════════════════════════════════════════════════
# CLASS: CentroidTracker
# Assigns a stable integer ID to each detected face across frames.
# Uses nearest-centroid matching; IDs survive brief disappearances.
# ══════════════════════════════════════════════════════════════════
class CentroidTracker:
    def __init__(self, max_disappeared=MAX_DISAPPEARED, max_dist=TRACK_DIST_MAX):
        self.next_id      = 0
        self.centroids    = {}          # face_id → (cx, cy)
        self.disappeared  = {}          # face_id → frames-missing count
        self.max_gone     = max_disappeared
        self.max_dist     = max_dist

    @staticmethod
    def _centroid(box):
        x1, y1, x2, y2 = box
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    def update(self, boxes):
        """
        boxes : list of (x1, y1, x2, y2) face boxes for this frame.
        Returns : dict { box_index → face_id }
        """
        # ── No detections: age all existing IDs ───────────────────
        if not boxes:
            for fid in list(self.disappeared):
                self.disappeared[fid] += 1
                if self.disappeared[fid] > self.max_gone:
                    del self.centroids[fid]
                    del self.disappeared[fid]
            return {}

        new_centroids = [self._centroid(b) for b in boxes]

        # ── First frame: register everything fresh ────────────────
        if not self.centroids:
            mapping = {}
            for i, c in enumerate(new_centroids):
                self.centroids[self.next_id]   = c
                self.disappeared[self.next_id] = 0
                mapping[i] = self.next_id
                self.next_id += 1
            return mapping

        # ── Match new centroids to existing ones (greedy nearest) ─
        existing_ids  = list(self.centroids.keys())
        existing_c    = np.array(list(self.centroids.values()), dtype=float)
        new_c         = np.array(new_centroids, dtype=float)

        # Euclidean distance matrix  [existing × new]
        diff  = existing_c[:, np.newaxis, :] - new_c[np.newaxis, :, :]
        dists = np.sqrt((diff ** 2).sum(axis=2))

        used_rows, used_cols = set(), set()
        mapping = {}

        # Sort all (row, col) pairs by distance ascending
        for row, col in sorted(
            np.ndindex(dists.shape), key=lambda rc: dists[rc]
        ):
            if row in used_rows or col in used_cols:
                continue
            if dists[row, col] > self.max_dist:
                break   # remaining distances are all larger — stop
            fid = existing_ids[row]
            self.centroids[fid]   = new_centroids[col]
            self.disappeared[fid] = 0
            mapping[col] = fid
            used_rows.add(row)
            used_cols.add(col)

        # Age unmatched existing IDs
        for row in set(range(len(existing_ids))) - used_rows:
            fid = existing_ids[row]
            self.disappeared[fid] += 1
            if self.disappeared[fid] > self.max_gone:
                del self.centroids[fid]
                del self.disappeared[fid]

        # Register genuinely new faces
        for col in set(range(len(boxes))) - used_cols:
            self.centroids[self.next_id]   = new_centroids[col]
            self.disappeared[self.next_id] = 0
            mapping[col] = self.next_id
            self.next_id += 1

        return mapping


# ══════════════════════════════════════════════════════════════════
# CLASS: FaceState
# Stores ALL per-face state: emotion history, lock logic, demographics.
# One instance lives in `face_states[face_id]`.
# ══════════════════════════════════════════════════════════════════
class FaceState:
    def __init__(self):
        self.history       = deque(maxlen=SMOOTHING_WINDOW)
        self.stable        = "Detecting..."   # currently displayed emotion
        self.candidate     = "Detecting..."   # emotion being evaluated for lock
        self.candidate_cnt = 0                # consecutive frames for candidate
        self.scores        = {}               # last raw DeepFace scores dict
        self.age           = ""
        self.gender        = ""

    def push(self, emotion):
        """Add a new prediction and update the stable (locked) label."""
        self.history.append(emotion)

        # Majority vote over rolling window
        majority = Counter(self.history).most_common(1)[0][0]

        # ── Emotion lock: only switch when majority is stable for
        #    LOCK_FRAMES consecutive rounds ──────────────────────
        if majority == self.candidate:
            self.candidate_cnt += 1
        else:
            self.candidate     = majority
            self.candidate_cnt = 1

        if self.candidate_cnt >= LOCK_FRAMES:
            self.stable = self.candidate


# ══════════════════════════════════════════════════════════════════
# HELPER: classify emotion from raw DeepFace scores
# ══════════════════════════════════════════════════════════════════
def classify_emotion(scores: dict) -> str:
    """
    Returns the most likely emotion label after applying:
      1. Confidence threshold  (reject if dominant < CONF_THRESHOLD)
      2. Ambiguity check       (reject if gap between top-2 is small)
    Falls back to "neutral" when either filter fires.
    """
    if not scores:
        return "neutral"

    sorted_emotions = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    top_emo,  top_conf  = sorted_emotions[0]
    _,        sec_conf  = sorted_emotions[1] if len(sorted_emotions) > 1 else ("", 0)

    # Reject weak confidence
    if top_conf < CONF_THRESHOLD:
        return "neutral"

    # Reject ambiguous predictions (happy vs neutral with similar scores)
    if (top_conf - sec_conf) < AMBIGUITY_MARGIN:
        return "neutral"

    return top_emo


# ══════════════════════════════════════════════════════════════════
# HELPER: draw per-face emotion confidence bar panel
# ══════════════════════════════════════════════════════════════════
def draw_bars(img, scores, origin_x, origin_y):
    """Horizontal bar chart for all 7 emotion scores anchored at origin."""
    if not scores:
        return
    BAR_MAX = 110
    BAR_H   = 13
    GAP     = 4
    LABEL_W = 68

    for i, (emo, pct) in enumerate(sorted(scores.items())):
        yt = origin_y + i * (BAR_H + GAP)
        c  = EMOTION_COLORS.get(emo, DEFAULT_COLOR)
        # track
        cv2.rectangle(img, (origin_x + LABEL_W, yt),
                      (origin_x + LABEL_W + BAR_MAX, yt + BAR_H), (45, 45, 45), -1)
        # fill
        cv2.rectangle(img, (origin_x + LABEL_W, yt),
                      (origin_x + LABEL_W + int(BAR_MAX * pct / 100), yt + BAR_H), c, -1)
        # label
        cv2.putText(img, f"{emo[:7]:7s}{pct:5.1f}%",
                    (origin_x, yt + BAR_H - 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.36, (210, 210, 210), 1, cv2.LINE_AA)


# ══════════════════════════════════════════════════════════════════
# INITIALISE MODELS
# ══════════════════════════════════════════════════════════════════
print("[INFO] Loading YOLOv8 model …")
yolo = YOLO("yolov8n.pt")   # auto-downloads on first run (~6 MB)

print("[INFO] Loading Haar Cascade face detector …")
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ══════════════════════════════════════════════════════════════════
# WEBCAM
# ══════════════════════════════════════════════════════════════════
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[ERROR] Cannot open webcam.")
    exit()

# Optional: bump resolution for better face quality
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ══════════════════════════════════════════════════════════════════
# STATE
# ══════════════════════════════════════════════════════════════════
tracker     = CentroidTracker()
face_states = {}          # face_id → FaceState
frame_count = 0
prev_time   = time.time()

print("[INFO] Emotion detection started. Press 'q' to quit.\n")

# ══════════════════════════════════════════════════════════════════
# MAIN LOOP
# ══════════════════════════════════════════════════════════════════
while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Frame grab failed.")
        break

    frame_count += 1
    h_frame, w_frame = frame.shape[:2]

    # ── FPS ───────────────────────────────────────────────────────
    now       = time.time()
    fps       = 1.0 / max(now - prev_time, 1e-6)
    prev_time = now

    # ══════════════════════════════════════════════════════════════
    # STAGE 1 — YOLO person detection
    # We ask YOLO to find class 0 (person) at low confidence so
    # partial heads are still picked up.
    # ══════════════════════════════════════════════════════════════
    yolo_results = yolo(frame, classes=[0], conf=0.35, verbose=False)

    person_boxes = []   # (x1, y1, x2, y2) clipped to frame
    for r in yolo_results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w_frame, x2), min(h_frame, y2)
            if (x2 - x1) > 40 and (y2 - y1) > 40:
                person_boxes.append((x1, y1, x2, y2))

    # ══════════════════════════════════════════════════════════════
    # STAGE 2 — Haar Cascade face detection inside each person crop
    # Two-stage approach: YOLO narrows the search region; Haar finds
    # the exact face rectangle within that region.
    # ══════════════════════════════════════════════════════════════
    face_boxes_abs = []   # face boxes in absolute frame coordinates

    for (px1, py1, px2, py2) in person_boxes:
        person_crop = frame[py1:py2, px1:px2]
        gray_crop   = cv2.cvtColor(person_crop, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray_crop,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(50, 50)
        )

        if len(faces) == 0:
            # Fallback: treat upper 45 % of person box as the face
            face_h = int((py2 - py1) * 0.45)
            face_boxes_abs.append((px1, py1, px2, py1 + face_h))
        else:
            for (fx, fy, fw, fh) in faces:
                face_boxes_abs.append((
                    px1 + fx,
                    py1 + fy,
                    px1 + fx + fw,
                    py1 + fy + fh
                ))

    # ══════════════════════════════════════════════════════════════
    # STAGE 3 — Centroid tracking
    # Assigns/maintains a stable face_id per detected face box.
    # ══════════════════════════════════════════════════════════════
    id_map = tracker.update(face_boxes_abs)   # { box_idx → face_id }

    # Initialise state for newly seen face IDs
    for face_id in id_map.values():
        if face_id not in face_states:
            face_states[face_id] = FaceState()

    # Purge state for IDs the tracker has retired
    active_ids = set(tracker.centroids.keys())
    for fid in list(face_states.keys()):
        if fid not in active_ids:
            del face_states[fid]

    # ══════════════════════════════════════════════════════════════
    # STAGE 4 — DeepFace emotion analysis (throttled by FRAME_SKIP)
    # Only runs every FRAME_SKIP frames to keep FPS high.
    # ══════════════════════════════════════════════════════════════
    run_deepface = (frame_count % FRAME_SKIP == 0)

    for box_idx, face_id in id_map.items():
        x1, y1, x2, y2 = face_boxes_abs[box_idx]
        state = face_states[face_id]

        if run_deepface:
            face_crop = frame[y1:y2, x1:x2]
            if face_crop.size == 0:
                continue
            try:
                analysis = DeepFace.analyze(
                    face_crop,
                    actions=["emotion", "age", "gender"],
                    enforce_detection=False,
                    silent=True
                )
                raw_scores = analysis[0]["emotion"]     # dict: emo → float%
                state.scores = raw_scores

                # ── Confidence + ambiguity filtering ─────────────
                detected = classify_emotion(raw_scores)

                # ── Push into per-face rolling history ────────────
                state.push(detected)

                # ── Store demographics ────────────────────────────
                state.age    = str(int(analysis[0].get("age", 0)))
                state.gender = analysis[0].get("dominant_gender", "")

            except Exception:
                pass   # bad crop / DeepFace hiccup — skip silently

        # ══════════════════════════════════════════════════════════
        # STAGE 5 — Draw overlays
        # ══════════════════════════════════════════════════════════
        color       = EMOTION_COLORS.get(state.stable, DEFAULT_COLOR)
        conf_val    = state.scores.get(state.stable, 0.0)
        label_text  = f"{state.stable.capitalize()}  {conf_val:.1f}%"
        id_text     = f"ID:{face_id}"

        # Face bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Emotion label with solid background
        (lw, lh), _ = cv2.getTextSize(
            label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.72, 2
        )
        cv2.rectangle(frame, (x1, y1 - lh - 16), (x1 + lw + 8, y1), color, -1)
        cv2.putText(frame, label_text,
                    (x1 + 4, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.72,
                    (0, 0, 0), 2, cv2.LINE_AA)

        # Face ID (small, top-right of box)
        cv2.putText(frame, id_text,
                    (x2 - 48, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48,
                    color, 1, cv2.LINE_AA)

        # Age / gender below the box
        if state.age and state.gender:
            cv2.putText(frame,
                        f"~{state.age} yrs  |  {state.gender}",
                        (x1, y2 + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.52,
                        color, 1, cv2.LINE_AA)

        # Per-face emotion bar chart (anchored inside / near the box)
        bar_x = x1
        bar_y = y2 + (32 if state.age else 10)
        if bar_y + 7 * 18 < h_frame:   # only draw if it fits in frame
            draw_bars(frame, state.scores, bar_x, bar_y)

    # ── Global FPS counter ────────────────────────────────────────
    cv2.putText(frame, f"FPS {fps:5.1f}",
                (w_frame - 110, h_frame - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                (200, 200, 200), 1, cv2.LINE_AA)

    # ── Face count ────────────────────────────────────────────────
    cv2.putText(frame, f"Faces: {len(face_boxes_abs)}",
                (w_frame - 110, h_frame - 32),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48,
                (180, 180, 180), 1, cv2.LINE_AA)

    cv2.imshow("Emotion Recognition  [q = quit]", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("[INFO] Quitting …")
        break

# ══════════════════════════════════════════════════════════════════
# CLEANUP
# ══════════════════════════════════════════════════════════════════
cap.release()
cv2.destroyAllWindows()