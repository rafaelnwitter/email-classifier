from app.services.classification_service import ClassificationService
from app.services.reply_service import ReplyService


def test_fallback_should_identify_productive_email() -> None:
    service = ClassificationService()
    result = service._fallback_result(
        "Preciso de atualização sobre o status do meu chamado."
    )

    assert result.category == "PRODUTIVO"
    assert result.confidence in ["ALTA", "MEDIA", "BAIXA"]
    assert result.suggested_reply == ReplyService.fallback_reply("PRODUTIVO")


def test_fallback_should_identify_unproductive_email() -> None:
    service = ClassificationService()
    result = service._fallback_result(
        "Muito obrigado pelo excelente suporte e feliz natal a todos."
    )

    assert result.category == "IMPRODUTIVO"
    assert result.confidence in ["ALTA", "MEDIA", "BAIXA"]
    assert result.suggested_reply == ReplyService.fallback_reply("IMPRODUTIVO")


def test_heuristic_should_default_to_productive_with_medium_confidence_when_unclear() -> None:
    service = ClassificationService()
    category, confidence = service._heuristic_category("Mensagem neutra sem contexto.")

    assert category == "PRODUTIVO"
    assert confidence == "MEDIA"
