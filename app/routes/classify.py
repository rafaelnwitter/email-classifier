from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.models.email_models import ClassificationResponse
from app.services.classification_service import ClassificationService
from app.services.file_service import FileService
from app.services.preprocessing_service import PreprocessingService

router = APIRouter()
classification_service = ClassificationService()


@router.post("/classify", response_model=ClassificationResponse)
async def classify_email(
    email_text: str = Form(default=""),
    email_file: UploadFile | None = File(default=None),
) -> ClassificationResponse:
    raw_text = email_text.strip()

    if email_file is not None and email_file.filename and email_file.filename.strip():
        try:
            extracted = await FileService.extract_text_from_upload(email_file)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        raw_text = extracted or raw_text

    if not raw_text:
        raise HTTPException(status_code=400, detail="Informe um texto ou envie um arquivo.")

    normalized_text = PreprocessingService.normalize_text(raw_text)
    result = classification_service.classify(normalized_text)

    return ClassificationResponse(
        original_text=raw_text,
        normalized_text=normalized_text,
        result=result,
    )