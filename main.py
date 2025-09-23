from controllers import user_controller
from dotenv import load_dotenv
load_dotenv()
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from helpers.lifespan import lifespan


app = FastAPI(
            lifespan=lifespan,
            title="Project Name", 
            version="1.0",)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(user_controller.router, prefix="/api", tags=['User'])
