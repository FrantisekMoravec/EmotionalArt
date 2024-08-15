from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class EmotionRecognitionUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Emotion Recognition')
        self.setGeometry(100, 100, 1280, 720)

        # Main layout
        self.layout = QtWidgets.QVBoxLayout()

        # Image layout
        self.image_layout = QtWidgets.QHBoxLayout()

        # Video feed label (camera)
        self.video_feed_label = QtWidgets.QLabel(self)
        self.video_feed_label.setFixedSize(640, 480)
        self.image_layout.addWidget(self.video_feed_label)

        # Generated image label
        self.generated_image_label = QtWidgets.QLabel(self)
        self.generated_image_label.setFixedSize(512, 512)
        self.image_layout.addWidget(self.generated_image_label)

        self.layout.addLayout(self.image_layout)

        # Button layout
        self.button_layout = QtWidgets.QHBoxLayout()

        self.show_log_button = QtWidgets.QPushButton('Show Emotion Log', self)
        self.button_layout.addWidget(self.show_log_button)

        self.show_avg_log_button = QtWidgets.QPushButton('Show Average Emotion Log', self)
        self.button_layout.addWidget(self.show_avg_log_button)

        self.generate_image_button = QtWidgets.QPushButton('Generate Random Image', self)
        self.button_layout.addWidget(self.generate_image_button)

        self.layout.addLayout(self.button_layout)

        # Emotions table
        self.emotions_table = QtWidgets.QTableWidget(self)
        self.emotions_table.setRowCount(7)
        self.emotions_table.setColumnCount(2)
        self.emotions_table.setHorizontalHeaderLabels(['Emotion', 'Value'])
        self.layout.addWidget(self.emotions_table)

        self.setLayout(self.layout)

    def update_frame(self, image):
        self.video_feed_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def update_generated_image(self, pixmap):
        self.generated_image_label.setPixmap(pixmap)

    def update_emotions(self, emotions):
        for i, (emotion, value) in enumerate(emotions.items()):
            self.emotions_table.setItem(i, 0, QtWidgets.QTableWidgetItem(emotion))
            self.emotions_table.setItem(i, 1, QtWidgets.QTableWidgetItem(f"{value:.2f}%"))

    def show_emotion_log(self, log_data):
        self.log_window = EmotionLogWindow(log_data)
        self.log_window.show()

    def show_avg_emotion_log(self, log_data):
        self.avg_log_window = EmotionLogWindow(log_data)
        self.avg_log_window.show()


class EmotionLogWindow(QtWidgets.QWidget):
    def __init__(self, log_data):
        super().__init__()
        self.setWindowTitle('Emotion Log')
        self.setGeometry(200, 200, 600, 400)

        # Layout
        self.layout = QtWidgets.QVBoxLayout()

        # Log table
        self.log_table = QtWidgets.QTableWidget(self)
        self.log_table.setRowCount(len(log_data))
        self.log_table.setColumnCount(8)
        self.log_table.setHorizontalHeaderLabels(
            ['Timestamp', 'Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'])

        for row_idx, entry in enumerate(log_data):
            self.log_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(entry['timestamp']))
            for col_idx, emotion in enumerate(['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']):
                self.log_table.setItem(row_idx, col_idx + 1,
                                       QtWidgets.QTableWidgetItem(f"{entry['emotions'].get(emotion, 0):.2f}%"))

        self.layout.addWidget(self.log_table)
        self.setLayout(self.layout)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = EmotionRecognitionUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
