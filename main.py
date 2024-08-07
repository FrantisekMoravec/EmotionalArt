# main.py
import cv2
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from deepface import DeepFace
from ui import EmotionRecognitionUI


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = EmotionRecognitionUI()
        self.setCentralWidget(self.ui)

        # Inicializace kamery
        self.cap = cv2.VideoCapture(0)

        # Timer pro aktualizaci snímků z kamery
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Analýza emocí
        try:
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotions = analysis[0]['emotion']
            # Aktualizace UI
            self.ui.update_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.ui.update_emotions(emotions)
        except Exception as e:
            print("Error in emotion analysis:", e)

    def closeEvent(self, event):
        self.cap.release()
        cv2.destroyAllWindows()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
