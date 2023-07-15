from passlib.context import CryptContext

# Password Hashing, from FastAPI documentation
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hashes users password
def hash(password: str):
    return pwd_context.hash(password)

# re-hashes the user input password and matches it with the users hashed password stored on db 
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)