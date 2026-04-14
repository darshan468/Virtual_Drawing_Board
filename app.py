import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)

def count_fingers(hand_landmarks, handedness_label):
    fingers = []

    # Thumb logic depends on whether the hand is labeled 'Right' or 'Left'
    if handedness_label == 'Right':
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
            fingers.append(1)
        else:
            fingers.append(0)
    else:
        if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
            fingers.append(1)
        else:
            fingers.append(0)

    # Other 4 fingers
    tips = [8, 12, 16, 20]
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

def generate_frames():
    try:
        mp_hands = mp.solutions.hands
        mp_draw = mp.solutions.drawing_utils
    except AttributeError:
        import mediapipe.python.solutions as solutions
        mp_hands = solutions.hands
        mp_draw = solutions.drawing_utils

    hands = mp_hands.Hands(max_num_hands=1)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    # White background for the digital whiteboard
    canvas = np.ones((480, 640, 3), dtype=np.uint8) * 255
    
    COLORS = [
        (255, 0, 255),   # Magenta
        (0, 165, 255),   # Orange
        (255, 255, 0),   # Cyan
        (0, 0, 255),     # Red
        (0, 200, 0),     # Green
        (255, 0, 0),     # Blue
        (0, 0, 0),       # Black
        (128, 0, 255),   # Purple
    ]
    color_idx = 0
    color = COLORS[color_idx]
    
    prev_x, prev_y = 0, 0
    prev_fingers = 0

    while True:
        success, img = cap.read()
        if not success:
            continue
            
        img = cv2.flip(img, 1)
        
        # Ensure image is exactly 640x480
        img = cv2.resize(img, (640, 480))

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                x = int(hand_landmarks.landmark[8].x * 640)
                y = int(hand_landmarks.landmark[8].y * 480)

                label = handedness.classification[0].label
                fingers = count_fingers(hand_landmarks, label)

                # 1 Finger: Drawing Mode
                if fingers == 1:
                    if prev_x == 0 and prev_y == 0:
                        prev_x, prev_y = x, y

                    cv2.line(canvas, (prev_x, prev_y), (x, y), color, 6)
                    prev_x, prev_y = x, y

                # 5 Fingers: Eraser Tool
                elif fingers == 5:
                    # Draw a WHITE circle on the canvas to "erase" (since canvas is white)
                    cv2.circle(canvas, (x, y), 40, (255, 255, 255), -1)
                    # Overlay a black ring on the video to show where the eraser is tracking
                    cv2.circle(img, (x, y), 40, (0, 0, 0), 2)
                    prev_x, prev_y = 0, 0
                    
                # 4 Fingers: Clear Entire Canvas
                elif fingers == 4:
                    if prev_fingers != 4:
                        canvas = np.ones((480, 640, 3), dtype=np.uint8) * 255
                    prev_x, prev_y = 0, 0

                # 2 Fingers: Change Color
                elif fingers == 2:
                    if prev_fingers != 2:
                        color_idx = (color_idx + 1) % len(COLORS)
                        color = COLORS[color_idx]
                    prev_x, prev_y = 0, 0

                else:
                    prev_x, prev_y = 0, 0
                    
                prev_fingers = fingers

        # STITCHING: Side-by-side array concatenation
        # Left side: Webcam with tracking (640x480)
        # Right side: Digital whiteboard (640x480)
        combined_frame = np.hstack((img, canvas))
        
        # Encode to JPEG for the fast web stream
        ret, buffer = cv2.imencode('.jpg', combined_frame)
        if not ret:
            continue
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
