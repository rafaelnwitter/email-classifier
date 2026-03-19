from app.services.preprocessing_service import PreprocessingService


def test_normalize_text_should_trim_and_reduce_spaces() -> None:
    raw = "Olá,\n\n   preciso   de   ajuda   com  o chamado.   "
    result = PreprocessingService.normalize_text(raw)
    assert result == "Olá, preciso de ajuda com o chamado."


def test_normalize_text_should_return_empty_string_when_input_is_whitespace() -> None:
    raw = "   \n\n   "
    result = PreprocessingService.normalize_text(raw)
    assert result == ""