import random
import string

def generate_random_email(domain: str) -> str:
    """
    Génère une adresse email aléatoire avec un nom d'utilisateur de 8 à 12 caractères.
    """
    length = random.randint(8, 12)
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{username}@{domain}"
