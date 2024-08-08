import cv2
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from emotion_recognition import detect_emotions
from emotion_logger import EmotionLogger
from ui import EmotionRecognitionUI

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = EmotionRecognitionUI()
        self.setCentralWidget(self.ui)

        # Inicializace loggeru emocí
        self.emotion_logger = EmotionLogger()

        # Inicializace kamery
        self.cap = cv2.VideoCapture(0)

        # Timer pro aktualizaci snímků z kamery
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # Spojení tlačítka s funkcí
        self.ui.show_log_button.clicked.connect(self.show_emotion_log)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Detekce emocí a aktualizace UI
        try:
            frame, emotions = detect_emotions(frame)
            self.emotion_logger.log_emotions(emotions)
            self.ui.update_frame(QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888))
            self.ui.update_emotions(emotions)
        except Exception as e:
            print("Error in emotion detection and analysis:", e)

    def show_emotion_log(self):
        log_data = self.emotion_logger.get_logged_emotions()
        self.ui.show_emotion_log(log_data)

    def closeEvent(self, event):
        self.emotion_logger.save_to_file()
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
