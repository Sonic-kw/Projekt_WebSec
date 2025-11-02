"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from handlers.database import init_db
from routes import auth, chat

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    client = await init_db()
    yield
    # Shutdown
    client.close()

# Create FastAPI app
app = FastAPI(title="Forum API", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(chat.router, tags=["Chat"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Forum API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)