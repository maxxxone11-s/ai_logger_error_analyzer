import json
import httpx

from app.core.config import settings

MODELS = [
    "poolside/laguna-m.1:free",
    "openai/gpt-oss-20b:free",
    "google/gemma-3-27b-it:free",
]

async def analyze_error(
    message: str,
    stack_trace: str | None,
    similar_errors: list[str] | None = None
) -> dict:
    similar_errors_text = "\n\n".join(similar_errors or [])

    prompt = f"""
You are a senior backend developer.

Analyze this error.

Current error message:
{message}

Current stack trace:
{stack_trace}

Similar previous errors:
{similar_errors_text}

Return ONLY valid JSON with this structure:
{{
    "summary": "short explanation",
    "possible_reason": "possible cause",
    "suggested_fix": "specific fix"
}}
"""
    
    last_error: str | None = None

    async with httpx.AsyncClient(timeout=60) as client:
        for model in MODELS:
            response = await client.post(
                settings.openrouter_base_url,
                headers={
                    "Authorization": f"Bearer {settings.openrouter_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
            )

            if response.status_code == 200:
                data = response.json()
                text = data["choices"][0]["message"]["content"]

                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return {
                        "summary": text,
                        "possible_reason": None,
                        "suggested_fix": "Model did not return valid JSON."
                    }
            
            last_error = f"{response.status_code}: {response.text}"

    raise RuntimeError(f"All OpenRouter models failed. Last error: {last_error}")