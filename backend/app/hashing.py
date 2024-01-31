from passlib.context import CryptContext

# Create an instance of CryptContext with the bcrypt hashing scheme
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    @staticmethod
    def bcrypt(password: str):
        # Hash the password using bcrypt
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(hashed, normal):
        # Verify the normal password against the hashed password
        return pwd_cxt.verify(normal, hashed)
