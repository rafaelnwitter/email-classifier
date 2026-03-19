# AutoU Email Classifier

Aplicação web para classificar **um email por vez** como **PRODUTIVO** ou **IMPRODUTIVO** e sugerir uma resposta automática.

## Objetivo do desafio

Esta solução foi construída para atender ao escopo do teste técnico da AutoU:

- receber o conteúdo de **uma única mensagem**
- classificar a mensagem como **Produtiva** ou **Improdutiva**
- exibir uma justificativa objetiva
- sugerir uma resposta automática
- oferecer uma interface web simples
- disponibilizar backend em Python com deploy

## Escopo funcional

A aplicação processa **uma entrada por vez**:

- texto colado manualmente
- arquivo `.txt` contendo uma única mensagem
- arquivo `.pdf` contendo uma única mensagem

> Observação: arquivos com vários emails não são tratados como lote. Todo o conteúdo enviado é interpretado como uma única entrada, o que está alinhado com o escopo do desafio.

## Funcionalidades

- Upload de arquivos `.txt` e `.pdf`
- Campo de texto manual
- Classificação automática em `PRODUTIVO` ou `IMPRODUTIVO`
- Justificativa da decisão
- Resposta sugerida
- Fallback heurístico quando a chave OpenAI não estiver configurada
- Testes automatizados com `pytest`

## Arquitetura

```txt
app/
├─ main.py
├─ config.py
├─ routes/
│  └─ classify.py
├─ models/
│  └─ email_models.py
├─ services/
│  ├─ classification_service.py
│  ├─ file_service.py
│  ├─ preprocessing_service.py
│  └─ reply_service.py
├─ static/
│  ├─ app.js
│  └─ style.css
└─ templates/
   └─ index.html
```

## Tecnologias

- Python
- FastAPI
- Jinja2
- HTML/CSS/JavaScript
- OpenAI API
- PyPDF
- Pytest

## Requisitos

Exemplo de `requirements.txt`:

```txt
fastapi==0.115.0
uvicorn[standard]==0.30.6
jinja2==3.1.4
python-multipart==0.0.9
pydantic==2.9.2
pydantic-settings==2.5.2
openai==1.51.0
pypdf==5.0.1
pytest==8.3.3
httpx==0.27.2
```

## Variáveis de ambiente

Exemplo de `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
APP_ENV=development
```

## Execução local

```bash
python -m venv .venv
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env

uvicorn app.main:app --reload
```

A aplicação ficará disponível em:

```txt
http://127.0.0.1:8000
```

## Estratégia de classificação

A solução usa abordagem híbrida:

1. **Pré-processamento** para normalizar o texto
2. **Heurística** para garantir robustez e fallback
3. **LLM** para classificar e gerar a resposta sugerida quando a chave OpenAI estiver configurada

### Definições

- **PRODUTIVO**: email com solicitação, ação, suporte, acompanhamento, atualização, validação ou necessidade objetiva de resposta
- **IMPRODUTIVO**: email sem demanda prática imediata, como agradecimentos, felicitações ou reconhecimento genérico

## Tratamento de arquivos

A aplicação aceita:

- `.txt`
- `.pdf`

Se nenhum arquivo válido for enviado, mas o campo de texto estiver preenchido, a classificação deve ocorrer normalmente com base no texto informado.

## Testes

Executar:

```bash
pytest
```

Cobertura sugerida:

- normalização de texto
- classificação heurística
- resposta fallback
- endpoint principal
- comportamento sem input
- envio apenas de texto
- upload `.txt`
- upload vazio
- rejeição de formato inválido

## Deploy no Render

Exemplo de `render.yaml`:

```yaml
services:
  - type: web
    name: autou-email-classifier
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: OPENAI_MODEL
        value: gpt-4.1-mini
```

### Importante sobre a OpenAI API Key

Para produção, o mais seguro é configurar `OPENAI_API_KEY` diretamente no painel do Render.

## Demonstração sugerida no vídeo

- mostrar o campo de texto com um email produtivo
- mostrar um email improdutivo
- mostrar upload de `.txt`
- explicar que a aplicação processa **uma mensagem por vez**
- explicar fallback heurístico + LLM
- mostrar que o app continua funcionando mesmo sem a chave da OpenAI

## Melhorias futuras

- histórico persistido
- feedback humano para reclassificação
- novas categorias
- painel de métricas
- processamento em lote, caso o escopo evolua

## Conclusão

A proposta prioriza clareza, robustez e aderência ao escopo do teste.  
Em vez de adicionar complexidade desnecessária, a aplicação entrega uma experiência objetiva, demonstrável e pronta para deploy.
