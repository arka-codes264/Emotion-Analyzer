from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import time
import threading

app = Flask(__name__)

# --- Initialize MediaPipe ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# --- Global variables ---
cap = None
running = False
focused_frames = 0
total_frames = 0
start_time = 0
attention_percentage = 0


def generate_frames():
    global cap, focused_frames, total_frames, attention_percentage, running

    while running:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)
        total_frames += 1
        focused = False

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_eye = face_landmarks.landmark[474:478]
                right_eye = face_landmarks.landmark[469:473]
                for lm in left_eye + right_eye:
                    x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
                focused = True

        if focused:
            focused_frames += 1

        attention_percentage = round((focused_frames / total_frames) * 100, 1)
        cv2.putText(frame, f"Attention: {attention_percentage}%", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/video')
def video():
    """Video stream route"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/start')
def start_tracking():
    """Start webcam session"""
    global cap, running, focused_frames, total_frames, start_time
    if not running:
        cap = cv2.VideoCapture(0)
        focused_frames = 0
        total_frames = 0
        start_time = time.time()
        running = True
        threading.Thread(target=generate_frames).start()
    return jsonify({"status": "started"})


@app.route('/stop')
def stop_tracking():
    """Stop webcam session"""
    global cap, running
    running = False
    if cap:
        cap.release()
    return jsonify({"status": "stopped"})


@app.route('/status')
def get_status():
    """Send live status (attention %, elapsed time)"""
    global attention_percentage, start_time, running
    elapsed = round(time.time() - start_time, 1) if running else 0
    return jsonify({
        "attention": attention_percentage,
        "time": elapsed,
        "running": running
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
