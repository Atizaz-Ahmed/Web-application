# services/event_manager.py

class QuizEventManager:
    def __init__(self):
        self.observers = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def notify(self, username, score):
        for obs in self.observers:
            obs.update(username, score)
