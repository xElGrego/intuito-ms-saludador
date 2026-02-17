import json
import os

from src.infrastructure.adapters.json_repository_adapter import JSONEmailRepositoryAdapter
from src.infrastructure.adapters.graph_adapter import MSGraphEmailAdapter
from src.application.email_use_case import SendBulkEmailsUseCase

def main():
    senders_config = None
    
    # 1. Try to load from Environment Variable (Best for Azure/GitHub)
    env_config = os.getenv("SENDERS_CONFIG")
    if env_config:
        try:
            senders_config = json.loads(env_config)
            print("Using configuration from SENDERS_CONFIG environment variable...")
        except json.JSONDecodeError:
            print("Error: SENDERS_CONFIG environment variable contains invalid JSON.")
            return

    # 2. Fallback to local file
    if not senders_config:
        try:
            with open("senders.json", "r") as f:
                senders_config = json.load(f)
                print("Using configuration from senders.json (Local Mode)...")
        except FileNotFoundError:
            if not env_config:
                print("Error: Configuration not found. Set SENDERS_CONFIG env var or create senders.json.")
                return
        except json.JSONDecodeError:
            print("Error: senders.json contains invalid JSON.")
            return

    if not senders_config:
        print("Error: No sender configurations found.")
        return

    email_sender = MSGraphEmailAdapter(senders_config=senders_config)
    
    email_repository = JSONEmailRepositoryAdapter(file_path="emails.json")

    use_case = SendBulkEmailsUseCase(
        email_sender=email_sender,
        email_repository=email_repository
    )

    use_case.execute()

if __name__ == "__main__":
    main()
