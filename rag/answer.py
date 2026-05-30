import os

from openai import OpenAI

from config import COMPANY_NAME, HF_CHAT_MODEL
from rag.hf_auth import require_hf_token
from rag.retrieve import retrieve

SYSTEM_PROMPT_TEMPLATE = """
You are an internal documentation assistant for {company}. Answer using ONLY the context below.

- Be concise and factual. Use bullets or numbered steps when the context describes a procedure.
- If the context lists products, people, or contracts, name them accurately.
- If the context does not contain the answer, say you do not have that information in the knowledge base.
- Do not invent employee names, contract values, or product features not in the context.

Context:
{context}
"""


def get_client():
    return OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=require_hf_token(),
    )


def answer_question(question: str, history: list | None = None):
    if history is None:
        history = []
    docs = retrieve(question, history)
    context = "\n\n".join(doc.page_content for doc in docs)
    system = SYSTEM_PROMPT_TEMPLATE.format(company=COMPANY_NAME, context=context)

    messages = [{"role": "system", "content": system}]
    for turn in history:
        if isinstance(turn, dict):
            role = turn.get("role")
            content = turn.get("content", "")
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": question})

    model = os.environ.get("HF_CHAT_MODEL", HF_CHAT_MODEL)
    response = get_client().chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
        max_tokens=700,
    )
    answer = (response.choices[0].message.content or "").strip()
    return answer, docs
