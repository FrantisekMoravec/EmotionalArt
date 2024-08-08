import json
from datetime import datetime


class EmotionLogger:
    def __init__(self, filename='emotions.json'):
        self.filename = filename
        self.data = []

    def log_emotions(self, emotions):
        timestamp = datetime.now().isoformat()
        self.data.append({'timestamp': timestamp, 'emotions': emotions})

    def save_to_file(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get_logged_emotions(self):
        return self.data
