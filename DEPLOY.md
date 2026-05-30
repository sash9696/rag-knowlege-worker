# Deploy Insurellm Docs RAG to Hugging Face

## 1. Create the Space

1. Go to https://huggingface.co/new-space
2. Name: **`insurellm-docs-rag`** (or change `projects.js` demo URL to match)
3. SDK: **Gradio**
4. Hardware: **CPU basic** (free)
5. Visibility: Public

## 2. Push this folder

From your machine (one-time):

```bash
cd /Users/sahil/Desktop/Ai-portfolio/docs-rag-space
git init
git add .
git commit -m "Insurellm docs RAG Space"
git remote add origin https://huggingface.co/spaces/sash007/insurellm-docs-rag
git push -u origin main
```

Or upload files in the Space **Files** tab (include `knowledge-base/` tree).

## 3. Secrets

**Settings → Variables and secrets:**

| Name | Value |
|------|--------|
| `HF_TOKEN` | Same token as Trend Research Agent |

Optional: `HF_CHAT_MODEL` = `moonshotai/Kimi-K2-Instruct-0905`

## 4. First build

- Space installs deps and runs `app.py`.
- First request triggers **ingest** (~76 markdown files → Chroma). Allow 2–5 minutes on cold start.
- Later starts reuse `chroma_db/.ready`.

## 5. Wire portfolio

Demo URL (after live):

`https://huggingface.co/spaces/sash007/insurellm-docs-rag`

Already set in `src/data/projects.js` — change slug if your Space name differs.
