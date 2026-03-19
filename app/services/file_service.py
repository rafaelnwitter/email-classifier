from io import BytesIO
from pypdf import PdfReader
from fastapi import UploadFile


class FileService:
    @staticmethod
    async def extract_text_from_upload(upload: UploadFile) -> str:
        filename = (upload.filename or "").strip().lower()
        content_type = (upload.content_type or "").strip().lower()

        if not filename:
            return ""

        if filename.endswith(".txt") or content_type == "text/plain":
            content = await upload.read()
            return content.decode("utf-8", errors="ignore").strip()

        if filename.endswith(".pdf") or content_type == "application/pdf":
            content = await upload.read()
            reader = PdfReader(BytesIO(content))
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(pages).strip()

        raise ValueError(
            f"Formato não suportado. Arquivo recebido: filename='{upload.filename}', content_type='{upload.content_type}'. Envie um arquivo .txt ou .pdf."
        )
