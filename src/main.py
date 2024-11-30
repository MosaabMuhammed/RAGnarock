from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

# Importing all routes from the routes directory
from routes.base import base_router

app = FastAPI()

app.include_router(base_router)