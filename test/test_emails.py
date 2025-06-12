import pytest
from src.email_generator import generate_random_email

def test_generate_random_email():
    domain = "example.com"
    email = generate_random_email(domain)
    assert email.endswith(f"@{domain}")
    user = email.split("@")[0]
    assert 8 <= len(user) <= 12
    assert user.isalnum()
