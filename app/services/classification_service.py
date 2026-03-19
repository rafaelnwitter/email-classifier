import json
from typing import Any
from openai import OpenAI

from app.config import settings
from app.models.email_models import ClassificationResult
from app.services.reply_service import ReplyService


PRODUCTIVE_KEYWORDS = {
    "status", "atualização", "erro", "problema", "suporte", "chamado",
    "requisição", "solicitação", "prazo", "anexo", "documento", "caso",
    "urgente", "pendente", "retorno", "analisar", "aprovação", "ajuda",
}

UNPRODUCTIVE_KEYWORDS = {
    "feliz natal", "parabéns", "obrigado", "obrigada", "agradeço",
    "agradecemos", "bom dia", "boa tarde", "boa noite", "felicitações",
}


class ClassificationService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def _heuristic_category(self, text: str) -> tuple[str, str]:
        normalized = text.lower()
        productive_hits = sum(1 for keyword in PRODUCTIVE_KEYWORDS if keyword in normalized)
        unproductive_hits = sum(1 for keyword in UNPRODUCTIVE_KEYWORDS if keyword in normalized)

        if productive_hits > unproductive_hits:
            return "PRODUTIVO", "ALTA"
        if unproductive_hits > productive_hits:
            return "IMPRODUTIVO", "ALTA"
        return "PRODUTIVO", "MEDIA"

    def _fallback_result(self, text: str) -> ClassificationResult:
        category, confidence = self._heuristic_category(text)
        reason = (
            "O email contém uma solicitação, acompanhamento ou demanda objetiva."
            if category == "PRODUTIVO"
            else "O email não apresenta uma demanda objetiva de ação imediata."
        )
        return ClassificationResult(
            category=category,
            reason=reason,
            suggested_reply=ReplyService.fallback_reply(category),
            confidence=confidence,
        )

    def classify(self, text: str) -> ClassificationResult:
        if not self.client:
            return self._fallback_result(text)

        prompt = (
            "Você é um classificador de emails corporativos. "
            "Classifique em PRODUTIVO ou IMPRODUTIVO. "
            "PRODUTIVO exige ação, resposta, acompanhamento, suporte ou atualização. "
            "IMPRODUTIVO não exige ação prática imediata, como felicitações ou agradecimentos genéricos. "
            "Retorne apenas JSON válido com: category, reason, suggested_reply, confidence. "
            "confidence deve ser ALTA, MEDIA ou BAIXA. "
            f"Email: {text}"
        )

        try:
            response = self.client.responses.create(
                model=settings.openai_model,
                input=prompt,
            )
            output_text = response.output_text
            payload: dict[str, Any] = json.loads(output_text)

            if "suggested_reply" not in payload or not payload["suggested_reply"]:
                payload["suggested_reply"] = ReplyService.fallback_reply(payload["category"])

            return ClassificationResult(**payload)
        except Exception:
            return self._fallback_result(text)