from dataclasses import dataclass
from typing import List

@dataclass
class EmailMessage:
    subject: str
    body: str

@dataclass
class Recipient:
    email: str
    name: str
