from typing import List
from src.domain.ports import EmailRepositoryPort
from src.domain.models import EmailMessage, Recipient
from src.core.config.app_settings import get_app_settings


class EnvEmailRepositoryAdapter(EmailRepositoryPort):
    def get_recipients(self) -> List[Recipient]:
        settings = get_app_settings()
        recipients_str = settings.email_recipients
        
        if not recipients_str:
            return []
        
        recipients = []
        for part in recipients_str.split(";"):
            if ":" in part:
                email, name = part.split(":", 1)
                recipients.append(Recipient(email=email.strip(), name=name.strip()))
        return recipients

    def get_template(self) -> EmailMessage:
        settings = get_app_settings()
        subject = settings.email_subject
        body = settings.email_body
        return EmailMessage(subject=subject, body=body)
