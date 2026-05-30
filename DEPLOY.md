# Deploy Knowledge Worker to Hugging Face

## 1. Create the Space

1. Go to https://huggingface.co/new-space
2. Name: **`knowledge-worker`**
3. SDK: **Gradio**
4. Hardware: **CPU basic** (free)
5. Visibility: Public
6. Link repo: `sash9696/rag-knowlege-worker` (or push files manually)

## 2. Push updates (if using HF git)

```bash
cd /Users/sahil/Desktop/Ai-portfolio/docs-rag-space
git add .
git commit -m "Rename to Knowledge Worker"
git push origin main
# If using HF remote:
git push space main
```

## 3. Secrets

**Settings → Variables and secrets:**

| Name | Value |
|------|--------|
| `HF_TOKEN` | Same token as Trend Research Agent |

Optional: `HF_CHAT_MODEL` = `moonshotai/Kimi-K2-Instruct-0905`

## 4. First build

- First chat triggers ingest (~76 docs → Chroma). Allow **2–5 minutes** on cold start.
- Later runs reuse `chroma_db/.ready`.

## 5. Live URL

`https://huggingface.co/spaces/sash007/knowledge-worker`

Update `src/data/projects.js` if your Space slug differs.
