import os, httpx

AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama")
AI_MODEL = os.getenv("AI_MODEL", "gemma3:1b")
AI_BASE_URL = os.getenv("AI_BASE_URL", "http://localhost:11434")
AI_API_KEY = os.getenv("AI_API_KEY", "")

def chat_json(system: str, user: str, images_b64: list[str] | None = None) -> str:
    if AI_PROVIDER == "ollama":
        msg = {"role": "user", "content": user}
        if images_b64:
            msg["images"] = images_b64
        r = httpx.post(
            f"{AI_BASE_URL}/api/chat",
            json={
                "model": AI_MODEL,
                "stream": False,
                "think": False,
                "format": "json",
                "options": {"temperature": 0.2, "num_ctx": 8192},
                "messages": [{"role": "system", "content": system}, msg],
            },
            timeout=300,
        )
        r.raise_for_status()
        return r.json()["message"]["content"]

    r = httpx.post(
        f"{AI_BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {AI_API_KEY}"},
        json={
            "model": AI_MODEL,
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        },
        timeout=90,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
