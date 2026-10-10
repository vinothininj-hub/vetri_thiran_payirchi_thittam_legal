from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import router
app = FastAPI(title="LegalEase API", version="1.0.0", description="AI-powered legal document drafting API.")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
@app.get("/")
def root(): return {"service":"LegalEase API","status":"running","docs":"/docs"}
app.include_router(router)
