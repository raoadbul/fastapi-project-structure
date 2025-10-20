from controllers import user_controller
from dotenv import load_dotenv
load_dotenv()
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile
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
@app.post("/media/upload/")
async def upload_file(file: UploadFile = File(...)):
    safe_filename = file.filename.replace(" ", "_")
    with open(f"media/{safe_filename}", "wb") as buffer:
        buffer.write(await file.read())
    return {"url": f"/media/{safe_filename}"}

app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(user_controller.router, prefix="/api", tags=['User'])
