from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime
from app.lib.environment import SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/")


def decode_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        uuid = payload.get("sub")
        expires_at = payload.get("exp")

        # if datetime.utcnow() > datetime.fromtimestamp(expires_at):
        #     raise Exception()
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    else:
        return uuid