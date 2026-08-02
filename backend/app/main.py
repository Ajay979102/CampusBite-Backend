from app.database.connection import engine
from sqlalchemy import text
from fastapi import FastAPI
from app.security.hashing import hash_password

app = FastAPI(
    title="CampusBite API",
    description="Backend API for CampusBite Smart Canteen System",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to CampusBite API 🚀"}

@app.get("/health")
def health():
    return {"status": "Server is running successfully!"}

@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return {
                "status": "success",
                "database": "Connected Successfully"
            }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }


@app.get("/hash-test")
def hash_test():
    password = "CampusBite123"
    hashed = hash_password(password)

    return {
        "original": password,
        "hashed": hashed
    }