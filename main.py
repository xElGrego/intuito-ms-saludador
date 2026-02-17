from src.core.config.app_settings import get_app_settings
from src.infrastructure.adapters.env_repository_adapter import EnvEmailRepositoryAdapter
from src.infrastructure.adapters.graph_adapter import MSGraphEmailAdapter
from src.application.email_use_case import SendBulkEmailsUseCase


def main():
    settings = get_app_settings()
    
    if not all([
        settings.sender_tenant_id, 
        settings.sender_client_id, 
        settings.sender_client_secret, 
        settings.sender_user_email
    ]):
        print("Error: Missing MS Graph configuration in environment variables.")
        print("Required: SENDER_TENANT_ID, SENDER_CLIENT_ID, SENDER_CLIENT_SECRET, SENDER_USER_EMAIL")
        return

    senders_config = [{
        "tenant_id": settings.sender_tenant_id,
        "client_id": settings.sender_client_id,
        "client_secret": settings.sender_client_secret,
        "user_email": settings.sender_user_email
    }]

    email_sender = MSGraphEmailAdapter(senders_config=senders_config)
    
    email_repository = EnvEmailRepositoryAdapter()

    use_case = SendBulkEmailsUseCase(
        email_sender=email_sender,
        email_repository=email_repository
    )

    use_case.execute()


if __name__ == "__main__":
    main()
