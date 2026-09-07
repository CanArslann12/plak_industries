import os

import requests

from config import BUSINESS_CONTEXT


class AIServiceError(Exception):
    """Raised when the configured AI provider cannot answer safely."""


class AIService:
    def __init__(self, api_key="", model="llama-3.1-8b-instant", timeout=20, business_context=""):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.business_context = business_context

    def yanit_uret(self, mesaj, gecmis):
        if not self.api_key:
            raise AIServiceError("AI sağlayıcısı yapılandırılmamış.")
        if not isinstance(gecmis, list):
            raise AIServiceError("Geçmiş biçimi geçersiz.")
        messages = [{"role": "system", "content": self.business_context}]
        for item in gecmis[-20:]:
            if isinstance(item, dict) and item.get("role") in ("user", "assistant") and isinstance(item.get("content"), str):
                messages.append({"role": item["role"], "content": item["content"][:4000]})
        messages.append({"role": "user", "content": mesaj[:4000]})
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": self.model, "messages": messages},
                timeout=self.timeout,
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            if not isinstance(content, str) or not content.strip():
                raise KeyError("content")
            return content.strip()
        except (requests.RequestException, ValueError, KeyError, IndexError, TypeError) as error:
            raise AIServiceError("AI sağlayıcısı yanıt vermedi.") from error


ai_service = AIService(
    api_key=os.getenv("GROQ_API_KEY", ""),
    model=os.getenv("AI_MODEL", "openai/gpt-oss-20b"),
    timeout=float(os.getenv("AI_TIMEOUT_SECONDS", "20")),
    business_context=BUSINESS_CONTEXT,
)