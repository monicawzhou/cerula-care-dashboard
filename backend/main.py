"""
App wiring only: create FastAPI app, bind database, mount routers.
"""
import models
from database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import patients_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(patients_router)
