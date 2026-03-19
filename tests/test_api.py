from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_should_return_success() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Classificador Inteligente de Emails" in response.text


def test_classify_should_fail_when_no_input_is_provided() -> None:
    response = client.post("/api/classify", data={"email_text": ""})

    assert response.status_code == 400
    assert response.json()["detail"] == "Informe um texto ou envie um arquivo."


def test_classify_should_return_result_when_text_is_provided() -> None:
    response = client.post(
        "/api/classify",
        data={
            "email_text": "Gostaria de saber o status da minha solicitação em andamento."
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["result"]["category"] in ["PRODUTIVO", "IMPRODUTIVO"]
    assert payload["result"]["suggested_reply"]


def test_classify_should_accept_text_without_real_file() -> None:
    response = client.post(
        "/api/classify",
        data={"email_text": "Preciso de atualização sobre o chamado aberto ontem."},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["result"]["category"] in ["PRODUTIVO", "IMPRODUTIVO"]


def test_classify_should_accept_txt_upload() -> None:
    response = client.post(
        "/api/classify",
        files={
            "email_file": (
                "email.txt",
                "Gostaria de saber o status do chamado aberto ontem.".encode("utf-8"),
                "text/plain",
            )
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["result"]["category"] == "PRODUTIVO"


def test_classify_should_reject_unsupported_file_type() -> None:
    response = client.post(
        "/api/classify",
        files={
            "email_file": (
                "email.docx",
                "conteudo invalido".encode("utf-8"),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    assert response.status_code == 400
    assert "Formato não suportado" in response.json()["detail"]