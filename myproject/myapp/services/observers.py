# services/observers.py

class QuizObserver:
    def update(self, username, score):
        pass


class EmailNotifier(QuizObserver):
    def update(self, username, score):
        pass

class Logger(QuizObserver):
    def __init__(self):
        self.message = ""

    def update(self, username, score):
        self.message = f"User {username} scored {score} points."
