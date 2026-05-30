---
title: Knowledge Worker
emoji: 📚
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 5.49.1
python_version: "3.12"
app_file: app.py
pinned: false
license: mit
short_description: RAG chat over a demo document corpus with sources panel
---

# Knowledge Worker

RAG pipeline: ingest markdown → Chroma → retrieve → answer (Hugging Face router).

**Secret required:** add under **Settings → Repository secrets** (not public Variables):

- Name: `HF_TOKEN`
- Value: your `hf_…` write token from [settings/tokens](https://huggingface.co/settings/tokens)
- Then **Factory restart** the Space
