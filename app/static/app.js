const form = document.getElementById("email-form");
const resultSection = document.getElementById("result");
const errorBox = document.getElementById("error-box");
const reasonEl = document.getElementById("reason");
const confidenceEl = document.getElementById("confidence");
const replyEl = document.getElementById("reply");
const badgeEl = document.getElementById("badge");
const copyReplyBtn = document.getElementById("copy-reply");
const emailText = document.getElementById("email_text");

const productiveSample =
  "Olá, gostaria de saber o status da minha requisição aberta ontem. Também envio em anexo o documento solicitado para continuidade do atendimento.";

const unproductiveSample =
  "Olá equipe, passando para agradecer o apoio de vocês nesta semana. Excelente trabalho e parabéns pelo resultado alcançado.";

document.getElementById("sample-productive").addEventListener("click", () => {
  emailText.value = productiveSample;
});

document.getElementById("sample-unproductive").addEventListener("click", () => {
  emailText.value = unproductiveSample;
});

copyReplyBtn.addEventListener("click", async () => {
  const text = replyEl.textContent || "";
  await navigator.clipboard.writeText(text);
  copyReplyBtn.textContent = "Copiado";
  setTimeout(() => {
    copyReplyBtn.textContent = "Copiar resposta";
  }, 1200);
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.classList.add("hidden");
  resultSection.classList.add("hidden");

  const formData = new FormData(form);

  try {
    const response = await fetch("/api/classify", {
      method: "POST",
      body: formData,
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "Erro ao processar o email.");
    }

    const { result } = payload;
    badgeEl.textContent = result.category;
    badgeEl.className = "badge " + (result.category === "PRODUTIVO" ? "productive" : "unproductive");
    reasonEl.textContent = result.reason;
    confidenceEl.textContent = result.confidence;
    replyEl.textContent = result.suggested_reply;
    resultSection.classList.remove("hidden");
  } catch (error) {
    errorBox.textContent = error.message || "Erro inesperado.";
    errorBox.classList.remove("hidden");
  }
});
