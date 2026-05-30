"""
Insurellm Docs RAG — Hugging Face Space
Chat over fictional insurance company docs (products, employees, contracts, company).
"""
import gradio as gr

from rag.answer import answer_question
from rag.ingest import ensure_vector_db


def format_context(docs):
    if not docs:
        return "*No context retrieved.*"
    parts = ["### Sources used\n"]
    for idx, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "?")
        name = source.split("/")[-1] if "/" in source else source
        score = doc.metadata.get("_score")
        header = f"**{idx}. {name}**"
        if isinstance(score, (int, float)):
            header += f" · score {score:.3f}"
        content = (doc.page_content or "").strip()
        preview = content[:500] + ("…" if len(content) > 500 else "")
        parts.append(f"{header}\n\n{preview}\n")
    return "\n".join(parts)


def chat(history):
    last_message = history[-1]["content"]
    prior = history[:-1]
    try:
        answer, docs = answer_question(last_message, prior)
    except Exception as e:
        answer = f"Sorry — something went wrong: {e}"
        docs = []
    history.append({"role": "assistant", "content": answer})
    return history, format_context(docs)


def build_ui():
    ensure_vector_db()

    def put_message_in_chatbot(message, history):
        return "", history + [{"role": "user", "content": message}]

    theme = gr.themes.Soft(primary_hue="cyan")

    with gr.Blocks(title="Insurellm Docs RAG", theme=theme) as ui:
        gr.Markdown(
            """
# Insurellm — internal docs Q&A
Ask about **products**, **employees**, **contracts**, and **company** info.
Answers are grounded in retrieved markdown chunks (demo corpus, not Robin).
            """
        )
        with gr.Row():
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(
                    label="Chat",
                    height=520,
                    type="messages",
                    show_copy_button=True,
                )
                message = gr.Textbox(
                    placeholder="e.g. What products does Insurellm offer?",
                    show_label=False,
                )
                gr.Examples(
                    examples=[
                        "What is Insurellm and what does the company do?",
                        "List the main insurance products in the knowledge base.",
                        "Who is Marcus Johnson and what is his role?",
                        "Which contracts mention Healthllm?",
                    ],
                    inputs=message,
                )
            with gr.Column(scale=1):
                context_markdown = gr.Markdown(
                    value="*Retrieved chunks appear here after each reply.*",
                    label="Retrieved context",
                )

        message.submit(
            put_message_in_chatbot,
            inputs=[message, chatbot],
            outputs=[message, chatbot],
        ).then(chat, inputs=chatbot, outputs=[chatbot, context_markdown])

    return ui


demo = build_ui()

if __name__ == "__main__":
    demo.launch()
