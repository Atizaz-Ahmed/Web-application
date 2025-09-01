# services/config.py

class QuizConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QuizConfig, cls).__new__(cls)
            cls._instance.load()
        return cls._instance

    def load(self):
        # These could be loaded from a DB in future
        self.allow_retake = False
        self.max_attempts = 7
