from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.database import engine, Base
from app.routers import students, attendance, enquiries, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (Alembic handles migrations in prod)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="BustleKidz API",
    description="School Management Platform — Bustle Kidz, Chennai",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(students.router, prefix="/students", tags=["students"])
app.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
app.include_router(enquiries.router, prefix="/enquiries", tags=["enquiries"])


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "service": "bustlekidz-api"}


@app.get("/", tags=["root"])
async def root():
    return {"message": "BustleKidz API", "docs": "/docs"}
