import os
import tempfile
from src.database import EmailDatabase

def test_add_and_list_and_delete():
    fd, path = tempfile.mkstemp()
    db = EmailDatabase(path)

    db.add_email("test1@example.com", "example.com")
    db.add_email("test2@example.org", "example.org")

    emails = db.list_emails()
    assert len(emails) == 2

    # Test recherche
    res = db.list_emails("example.com")
    assert len(res) == 1
    assert res[0][1] == "test1@example.com"

    # Suppression
    email_id = emails[0][0]
    db.delete_email(email_id)
    emails_after = db.list_emails()
    assert len(emails_after) == 1

    os.close(fd)
    os.remove(path)
