import json
from typing import List
from src.domain.ports import EmailRepositoryPort
from src.domain.models import EmailMessage, Recipient

class JSONEmailRepositoryAdapter(EmailRepositoryPort):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _load_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_recipients(self) -> List[Recipient]:
        data = self._load_data()
        return [Recipient(email=r['email'], name=r['name']) for r in data['recipients']]

    def get_template(self) -> EmailMessage:
        data = self._load_data()
        template = data['template']
        return EmailMessage(subject=template['subject'], body=template['body'])
