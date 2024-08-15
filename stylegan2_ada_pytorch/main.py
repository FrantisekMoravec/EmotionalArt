import cv2
import sys

from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from emotion_recognition import detect_emotions
from emotion_logger import EmotionLogger
from generate_image import initialize_and_generate_image, save_image, create_run_directory
from ui import EmotionRecognitionUI
from PyQt5.QtGui import QPixmap


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = EmotionRecognitionUI()
        self.setCentralWidget(self.ui)

        # Emotion logging
        self.emotion_logger = EmotionLogger()

        # Creating directories
        self.run_directory = create_run_directory()

        # Cam initialisation
        self.cap = cv2.VideoCapture(0)

        # Timer for camera images
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # Giving buttons a purpose
        self.ui.show_log_button.clicked.connect(self.show_emotion_log)
        self.ui.show_avg_log_button.clicked.connect(self.show_avg_emotion_log)
        self.ui.generate_image_button.clicked.connect(self.generate_and_display_image)

        # Displaying generated image
        self.generate_and_display_image()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        try:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb, emotions = detect_emotions(frame_rgb)
            self.emotion_logger.log_emotions(emotions)
            image = QtGui.QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], frame_rgb.strides[0], QtGui.QImage.Format_RGB888)
            self.ui.update_frame(image)
            self.ui.update_emotions(emotions)
        except Exception as e:
            print("Error in emotion detection and analysis:", e)

    def generate_and_display_image(self):
        model_path = '../pretrained_models/afhqcat.pkl'
        generated_image = initialize_and_generate_image(model_path)

        image_path = save_image(generated_image, self.run_directory, 'random_image.png')
        qt_pixmap = QPixmap(image_path)

        # Updating generated image
        self.ui.update_generated_image(qt_pixmap)

    def show_emotion_log(self):
        log_data = self.emotion_logger.get_logged_emotions()
        self.ui.show_emotion_log(log_data)

    def show_avg_emotion_log(self):
        avg_log_data = self.emotion_logger.get_avg_logged_emotions()
        self.ui.show_avg_emotion_log(avg_log_data)

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
