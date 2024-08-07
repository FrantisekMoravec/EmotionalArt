# ui.py
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class EmotionRecognitionUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Emotion Recognition')
        self.setGeometry(100, 100, 800, 600)

        # Layout
        self.layout = QtWidgets.QVBoxLayout()

        # Video feed label
        self.video_feed_label = QtWidgets.QLabel(self)
        self.video_feed_label.setFixedSize(640, 480)
        self.layout.addWidget(self.video_feed_label)

        # Emotions label
        self.emotions_label = QtWidgets.QLabel(self)
        self.emotions_label.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.emotions_label)

        self.setLayout(self.layout)

    def update_frame(self, frame):
        image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.video_feed_label.setPixmap(pixmap)

    def update_emotions(self, emotions):
        emotions_text = "\n".join([f"{emotion}: {value:.2f}%" for emotion, value in emotions.items()])
        self.emotions_label.setText(emotions_text)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = EmotionRecognitionUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
