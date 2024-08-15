import json
from datetime import datetime, timedelta


class EmotionLogger:
    def __init__(self, filename='emotions.json', avg_filename='avg_emotions.json'):
        self.filename = filename
        self.avg_filename = avg_filename
        self.data = []
        self.avg_data = []
        self.current_window = []
        self.window_start_time = datetime.now()

    def log_emotions(self, emotions):
        timestamp = datetime.now().isoformat()
        self.data.append({'timestamp': timestamp, 'emotions': emotions})

        # Logging emotions
        self.current_window.append(emotions)
        if datetime.now() - self.window_start_time >= timedelta(seconds=0.5):
            avg_emotions = self.average_emotions(self.current_window)
            self.avg_data.append({'timestamp': self.window_start_time.isoformat(), 'emotions': avg_emotions})
            self.current_window = []
            self.window_start_time = datetime.now()

    def average_emotions(self, emotions_list):
        avg_emotions = {}
        if emotions_list:
            keys = emotions_list[0].keys()
            for key in keys:
                avg_emotions[key] = sum(emotion[key] for emotion in emotions_list) / len(emotions_list)
        return avg_emotions

    def save_to_file(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)
        with open(self.avg_filename, 'w') as f:
            json.dump(self.avg_data, f, indent=4)

    def get_logged_emotions(self):
        return self.data

    def get_avg_logged_emotions(self):
        return self.avg_data
