# emotion_recognition.py
import cv2
from deepface import DeepFace

# Inicializace kamery
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame from camera. Exiting...")
        break

    # Analýza emocí
    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotions = analysis[0]['emotion']  # správný přístup k analýze emocí
        print("Emotions detected:", emotions)

        # Zobrazení výsledku
        dominant_emotion = max(emotions, key=emotions.get)
        cv2.putText(frame, dominant_emotion, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Emotion Recognition', frame)
    except Exception as e:
        print("Error in emotion analysis:", e)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
