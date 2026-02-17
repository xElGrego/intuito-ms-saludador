from abc import ABC, abstractmethod
from typing import List
from .models import EmailMessage, Recipient

class EmailSenderPort(ABC):
    @abstractmethod
    def send(self, recipient: Recipient, message: EmailMessage) -> bool:
        pass

class EmailRepositoryPort(ABC):
    @abstractmethod
    def get_recipients(self) -> List[Recipient]:
        pass

    @abstractmethod
    def get_template(self) -> EmailMessage:
        pass
