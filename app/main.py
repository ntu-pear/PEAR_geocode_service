from fastapi import FastAPI,Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routers import (geocode_router)
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="NTU FYP PEAR GEOCODE SERVICE",
    description="This is the geocode service api docs",
    version="1.0.0",
    servers=[],  # This removes the servers dropdown in Swagger UI
)


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:5173",
    os.getenv("WEB_FE_ORIGIN"),
    # Add other origins if needed
]


# middleware to connect to the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(geocode_router.router, prefix="/api/v1", tags=["geocode"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Geocode API Testing"}
