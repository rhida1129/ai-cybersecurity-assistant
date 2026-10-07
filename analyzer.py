import json
import requests

from pydantic import BaseModel, Field


BASE_URL = "http://localhost:1234/v1"
MODEL = "qwen/qwen3.5-9b"


class SecurityAnalysis(BaseModel):
    threat: str
    severity: str
    confidence: float = Field(ge=0.0, le=1.0)
    observed_facts: list[str]
    inferences: list[str]
    unknowns: list[str]
    recommendations: list[str]


def analyze_security_event(event: str) -> SecurityAnalysis:
    """
    Send a cybersecurity event to the local LLM
    and return a validated cybersecurity analysis.
    """

    url = f"{BASE_URL}/chat/completions"

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an AI cybersecurity analyst assisting a security professional. "
                    "Analyze security events using an evidence-first approach. "
                    "Do not invent facts that are not present in the event. "
                    "Clearly distinguish observed facts from inferences and unknown information. "
                    "Identify the most likely threat, estimate severity, provide a confidence "
                    "score from 0.0 to 1.0, and recommend defensive actions. "
                    "Return ONLY valid JSON. Do not use Markdown, code fences, or explanatory text "
                    "outside the JSON object. "
                    "The JSON must contain exactly these fields: "
                    "threat, severity, confidence, observed_facts, inferences, unknowns, recommendations. "
                    "severity must be one of: Low, Medium, High, Critical. "
                    "confidence must be a number between 0.0 and 1.0. "
                    "observed_facts, inferences, unknowns, and recommendations must each be arrays of strings."
                ),
            },
            {
                "role": "user",
                "content": event,
            },
        ],
        "temperature": 0.2,
    }

    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()

    content = data["choices"][0]["message"]["content"]

    analysis = SecurityAnalysis.model_validate(json.loads(content))

    return analysis


if __name__ == "__main__":
    result = analyze_security_event(
        "A Windows computer received 500 failed login attempts "
        "from the same external IP address within 5 minutes."
    )

    print("\n=== STRUCTURED CYBERSECURITY ANALYSIS ===\n")
    print(json.dumps(result.model_dump(), indent=2))