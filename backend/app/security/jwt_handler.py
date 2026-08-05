from jose import jwt
from datetime import datetime, timedelta

# Secret Key
SECRET_KEY = "campusbite_super_secret_key_2026"

# JWT Algorithm
ALGORITHM = "HS256"

# Token Expiry
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt