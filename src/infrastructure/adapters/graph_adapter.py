import msal
import requests
from typing import List, Dict, Any
from src.domain.ports import EmailSenderPort
from src.domain.models import EmailMessage, Recipient

class MSGraphEmailAdapter(EmailSenderPort):
    def __init__(self, senders_config: List[Dict[str, Any]]):
        self.senders_config = senders_config
        self.current_sender_index = 0

    def _get_access_token(self, config: Dict[str, Any]):
        app = msal.ConfidentialClientApplication(
            config['client_id'],
            authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
            client_credential=config['client_secret'],
        )
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" in result:
            return result['access_token']
        else:
            raise Exception(f"Could not acquire token: {result.get('error_description')}")

    def send(self, recipient: Recipient, message: EmailMessage) -> bool:
        config = self.senders_config[self.current_sender_index]
        self.current_sender_index = (self.current_sender_index + 1) % len(self.senders_config)

        try:
            token = self._get_access_token(config)
            
            body_content = message.body.replace("{name}", recipient.name)
            
            email_data = {
                "message": {
                    "subject": message.subject,
                    "body": {
                        "contentType": "Text",
                        "content": body_content
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address": recipient.email
                            }
                        }
                    ]
                },
                "saveToSentItems": "true"
            }

            user_email = config['user_email']
            endpoint = f"https://graph.microsoft.com/v1.0/users/{user_email}/sendMail"
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            response = requests.post(endpoint, json=email_data, headers=headers)
            
            if response.status_code == 202:
                return True
            else:
                print(f"Graph API Error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Graph Connection Error: {e}")
            return False
