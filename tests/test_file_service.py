import io

import pytest
from fastapi import UploadFile

from app.services.file_service import FileService


@pytest.mark.asyncio
async def test_extract_text_from_txt_upload() -> None:
    upload = UploadFile(
        filename="email.txt",
        file=io.BytesIO("Olá, preciso de ajuda com meu chamado.".encode("utf-8")),
    )

    content = await FileService.extract_text_from_upload(upload)

    assert "preciso de ajuda" in content.lower()


@pytest.mark.asyncio
async def test_extract_text_from_empty_filename_should_return_empty_string() -> None:
    upload = UploadFile(
        filename="",
        file=io.BytesIO("conteudo qualquer".encode("utf-8")),
    )

    content = await FileService.extract_text_from_upload(upload)

    assert content == ""


@pytest.mark.asyncio
async def test_extract_text_should_raise_for_unsupported_extension() -> None:
    upload = UploadFile(
        filename="email.docx",
        file=io.BytesIO("conteudo qualquer".encode("utf-8")),
    )

    with pytest.raises(ValueError, match="Formato não suportado"):
        await FileService.extract_text_from_upload(upload)