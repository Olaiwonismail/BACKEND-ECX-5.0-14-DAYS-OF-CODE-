# tests/test_auth.py
import pytest
from app.auth import hash_password, verify_password, create_token, decode_token
from datetime import timedelta

def test_password_hashing():
    password = "securepassword123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_token_creation_decoding():
    email = "test@example.com"
    token = create_token({"sub": email}, timedelta(minutes=15))
    payload = decode_token(token)
    assert payload["sub"] == email