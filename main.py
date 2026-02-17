import json
from src.infrastructure.adapters.json_repository_adapter import JSONEmailRepositoryAdapter
from src.infrastructure.adapters.graph_adapter import MSGraphEmailAdapter
from src.application.email_use_case import SendBulkEmailsUseCase

def main():
    try:
        with open("senders.json", "r") as f:
            senders_config = json.load(f)
            print("Using configuration from senders.json (Local Mode)...")
    except FileNotFoundError:
        print("Error: senders.json file not found and no Env Vars set.")
        return
    except json.JSONDecodeError:
        print("Error: senders.json contains invalid JSON.")
        return

    if not senders_config:
        print("Error: No sender configurations found in senders.json.")
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
