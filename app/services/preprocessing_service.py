import re


class PreprocessingService:
    @staticmethod
    def normalize_text(text: str) -> str:
        cleaned = text.replace("\r", " ").replace("\n", " ")
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned.strip()
    