from dotenv import load_dotenv
load_dotenv()
import os

TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["aerich.models", "models.user"],
            "default_connection": "default",
        },
    },
}