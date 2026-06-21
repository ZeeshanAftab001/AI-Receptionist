from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import agent_router,voice_router
from core import settings

app=FastAPI(title="AI Receptionist")

app.add_middleware(CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.ALLOWED_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"])

app.include_router(agent_router)
app.include_router(voice_router)


@app.get("/")
async def root():
    return {"message": "AI Receptionist API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__": 
    import uvicorn 
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)