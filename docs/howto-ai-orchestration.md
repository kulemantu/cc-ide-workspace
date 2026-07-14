# How to: AI Orchestration

This workspace has a managed Python environment with dependency management. That makes it straightforward to call external AI platforms — OpenRouter, OpenAI, image generators, vision APIs — from scripts that Claude writes and runs.

## The pattern

1. You ask Claude to do something that requires an external AI (generate images, transcribe audio, classify documents)
2. Claude adds the API client as a dependency: `uv add openai` or `uv add httpx`
3. Claude writes a script in `scripts/src/` that calls the API
4. API credentials go in `.local/` or as environment variables
5. Output goes to `workspace/<subfolder>/.outputs/`

## Adding API clients

From the `scripts/` directory, Claude runs:

```bash
uv add openai          # OpenAI / OpenRouter
uv add httpx           # Generic HTTP client for any REST API
uv add pillow          # Image processing
uv add python-pptx     # PowerPoint generation
uv add pandas          # Data analysis
```

Dependencies are tracked in `scripts/pyproject.toml` and locked in `scripts/uv.lock` — both committed to git, so your team gets the same environment.

## Credentials

API keys and tokens go in `.local/` — never committed:

```
.local/
├── openrouter-key.txt
├── openai-key.txt
└── credentials.env
```

Or use environment variables. Claude can read `.env` files from `.local/`.

## Prompt-as-code

When working with LLM APIs, prompts should be versioned code — not throwaway strings:

```python
# scripts/src/prompts.py
ANALYSIS_PROMPT = """
You are a data analyst. Given the following CSV data:
{data}

Provide:
1. A summary of key trends
2. Anomalies or outliers
3. Recommended next steps
"""
```

This makes prompts testable, reviewable in PRs, and improvable over time. Claude can iterate on prompts across sessions because they persist in `scripts/src/`.

## Provider-agnostic approach

Write scripts that accept a provider as a parameter:

```python
def call_llm(prompt: str, provider: str = "openrouter") -> str:
    """Call an LLM with the given prompt. Supports openrouter, openai, ollama."""
    ...
```

This lets you swap between OpenRouter (many models), OpenAI (GPT), and Ollama (local) without rewriting logic.

## Example: Image generation

> "Generate a cover image for my presentation using OpenRouter"

Claude would:
1. Add `httpx` to dependencies
2. Write `scripts/src/image_gen.py` with `--prompt`, `--output`, `--model` flags
3. Read the API key from `.local/openrouter-key.txt`
4. Save the image to `workspace/<subfolder>/.outputs/cover-image.png`
5. Write a test in `scripts/tests/test_image_gen.py`

## Output

All generated content goes to `workspace/<subfolder>/.outputs/`:
- Generated images
- Transcriptions
- Analysis reports
- Translated documents
- Extracted data

This keeps AI-generated artifacts in the user's space, separate from the code that produced them.
