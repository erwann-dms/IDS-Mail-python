from typing import List, Tuple, Optional
from .database import EmailDatabase
from .email_generator import generate_random_email

class EmailManager:
    def __init__(self, db_path: str = "emails.db"):
        self.db = EmailDatabase(db_path)

    def generate_emails(self, domain: str, count: int) -> List[str]:
        emails = []
        for _ in range(count):
            email = generate_random_email(domain)
            self.db.add_email(email, domain)
            emails.append(email)
        return emails

    def get_emails(self, search: Optional[str] = None) -> List[Tuple[int, str, str, str]]:
        return self.db.list_emails(search)

    def delete_email(self, email_id: int):
        self.db.delete_email(email_id)
