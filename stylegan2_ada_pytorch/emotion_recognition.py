import cv2
import mediapipe as mp
from deepface import DeepFace
import numpy as np

def draw_landmarks(frame, landmarks):
    for point in landmarks:
        cv2.circle(frame, (int(point[0]), int(point[1])), 1, (0, 255, 0), -1)

def detect_emotions(frame):
    # Initialising MediaPipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:

        # Converting image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Face detection
        results = face_mesh.process(rgb_frame)

        emotions = {}
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())

                # Face bounding box
                ih, iw, _ = frame.shape
                bbox = [np.min(np.array([[lm.x * iw, lm.y * ih] for lm in face_landmarks.landmark]), axis=0).astype(int),
                        np.max(np.array([[lm.x * iw, lm.y * ih] for lm in face_landmarks.landmark]), axis=0).astype(int)]
                x, y = bbox[0]
                w, h = bbox[1] - bbox[0]

                face_region = frame[y:y + h, x:x + w]

                # Emotion analysis
                try:
                    analysis = DeepFace.analyze(face_region, actions=['emotion'], enforce_detection=False)
                    emotions = analysis[0]['emotion']
                    dominant_emotion = max(emotions, key=emotions.get)

                    # Drawing dominant emotion
                    cv2.putText(frame, dominant_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)
                except Exception as e:
                    print("Error in emotion analysis:", e)

        return frame, emotions
