from fastapi import FastAPI

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