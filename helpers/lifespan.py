from tortoise import Tortoise
from helpers.tortoise_config import TORTOISE_ORM

async def lifespan(_):
    await Tortoise.init(TORTOISE_ORM)
    yield
    print("Ended")