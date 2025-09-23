from tortoise.models import Model
from tortoise import fields
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Model):

    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    is_verified = fields.BooleanField(default=False)
    step = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        """Verify a plain password against the hashed one."""
        return pwd_context.verify(plain_password, self.password)
             