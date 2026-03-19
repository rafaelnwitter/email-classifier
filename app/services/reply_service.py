from app.models.email_models import Category


class ReplyService:
    @staticmethod
    def fallback_reply(category: Category) -> str:
        if category == "PRODUTIVO":
            return (
                "Olá, recebemos sua mensagem e vamos analisar a solicitação. "
                "Retornaremos em breve com a atualização ou com os próximos passos."
            )

        return "Olá, agradecemos sua mensagem e o contato. Ficamos à disposição."
    