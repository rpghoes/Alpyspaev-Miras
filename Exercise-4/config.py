# config.py
from datetime import timedelta

SECRET_KEY = "your_secret_key"  # ����� ������������ ����� os.urandom ��� secrets.token_urlsafe()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
