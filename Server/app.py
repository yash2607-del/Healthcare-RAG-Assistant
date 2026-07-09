from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router

app = FastAPI(title="Lord Diagnostics AI API", description="Backend API for the RAG Assistant")

# Setup CORS so the external website can communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you should restrict this to your actual website domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our API routes
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    # Run the server on port 8000
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
