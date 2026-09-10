# auth.py
from passlib.context import CryptContext
from datetime import datetime,timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt,JWTError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security_scheme = HTTPBearer()

def obtener_fisioterapeuta_actual(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

SECRET_KEY = "Modifica esto"
ALGORITHM = "HS256"
EXPIRACIO_MINUTOS = 60

def crear_token(email: str)->str:
    expira=datetime.utcnow()+timedelta(minutes=EXPIRACIO_MINUTOS)
    datos={"sub":email,"exp":expira}
    return jwt.encode(datos,SECRET_KEY,algorithm=ALGORITHM)

#reescribe la contraseña que escribio el usuario 
def hashear_password(password: str) -> str:
    return pwd_context.hash(password)

#cuando alguien intenta hacer login, compara lo que escribió contra el hash guardado, y regresa true o false
def verificar_password(password_plano: str, password_hash: str) -> bool:
    return pwd_context.verify(password_plano, password_hash)

def obtener_fisioterapeuta_actual(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")