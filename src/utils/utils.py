from passlib.context import CryptContext

# password hashing ----------------------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash(password : str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    # responsible for comparing the two hashed passwords
    return pwd_context.verify(plain_password, hashed_password)



