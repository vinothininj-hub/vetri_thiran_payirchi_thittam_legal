from fastapi import APIRouter, HTTPException
from backend.schemas import DocumentRequest, DocumentResponse
from backend.services.generator import GeminiDocumentGenerator
from core.config import get_settings
router = APIRouter()
settings = get_settings()
generator = GeminiDocumentGenerator(settings)

@router.get("/health")
def health():
    return {"status":"ok","service":"LegalEase API","ai_mode":"mock" if settings.mock_ai else "gemini","model":settings.gemini_model}

@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    try:
        content = generator.generate(request.document_type, request.parties, request.terms, request.effective_date)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Generation failed: {exc}") from exc
    return DocumentResponse(document_type=request.document_type, content=content[:settings.max_document_chars], model="mock" if settings.mock_ai else settings.gemini_model)
