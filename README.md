# rag-knowlege-worker

RAG chat over the **Insurellm** demo corpus (fictional insurance company): products, employees, contracts, and company markdown from the LLM engineering course. **No Robin docs.**

- **Ingest:** load `.md` → chunk → embed (sentence-transformers) → Chroma  
- **Query:** retrieve chunks → answer with Hugging Face router (`HF_TOKEN`)  
- **UI:** Gradio chat + sources panel  

## Run locally

```bash
pip install -r requirements.txt
export HF_TOKEN=hf_...   # https://huggingface.co/settings/tokens
python app.py
```

First run builds `chroma_db/` (~1–3 min).

## Deploy on Hugging Face

See [DEPLOY.md](./DEPLOY.md). Suggested Space: `sash007/insurellm-docs-rag`.

## Secrets

| Variable | Required |
|----------|----------|
| `HF_TOKEN` | Yes |
| `HF_CHAT_MODEL` | Optional (default: `moonshotai/Kimi-K2-Instruct-0905`) |
