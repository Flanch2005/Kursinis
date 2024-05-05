from abc import ABC, abstractmethod


class Reminder(ABC):
    # Abstraktus metodas
    @abstractmethod
    def send_reminder(self, user):
        pass
