from fastapi import FastAPI
from app.router import router

app = FastAPI(
    title="Simple AI Question API",
    description="A simple FastAPI app for handling AI questions",
    version="1.0.0"
)

# Include the router
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to Simple AI Question API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}