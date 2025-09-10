from fastapi import FastAPI
from app.router import router, root_router

app = FastAPI(
    title="Simple AI Question API",
    description="A simple FastAPI app for handling AI questions",
    version="1.0.0",
)

# Include the routers
app.include_router(root_router)  # Root and health endpoints
app.include_router(router)  # API v1 endpoints
