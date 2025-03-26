import secrets
import string


def generate_reference_id():
    characters = string.ascii_letters + string.digits 
    return ''.join(secrets.choice(characters) for _ in range(8))