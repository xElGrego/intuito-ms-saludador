from src.domain.ports import EmailSenderPort, EmailRepositoryPort

class SendBulkEmailsUseCase:
    def __init__(self, email_sender: EmailSenderPort, email_repository: EmailRepositoryPort):
        self.email_sender = email_sender
        self.email_repository = email_repository

    def execute(self):
        recipients = self.email_repository.get_recipients()
        message_template = self.email_repository.get_template()
        
        success_count = 0
        for recipient in recipients:
            if self.email_sender.send(recipient, message_template):
                print(f"Successfully sent to: {recipient.email}")
                success_count += 1
            else:
                print(f"Failed to send to: {recipient.email}")
        
        print(f"Process finished. Successfully sent: {success_count}/{len(recipients)}")
