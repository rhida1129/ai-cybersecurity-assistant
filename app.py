from fastapi import FastAPI
from pydantic import BaseModel

from analyzer import analyze_security_event


app = FastAPI(
    title="AI Cybersecurity Assistant",
    description="Local LLM-powered cybersecurity event analysis API",
    version="1.0.0",
)


class SecurityEvent(BaseModel):
    event: str


@app.get("/")
def root():
    return {
        "name": "AI Cybersecurity Assistant",
        "status": "running",
        "llm": "local",
    }


@app.post("/analyze")
def analyze(event: SecurityEvent):
    analysis = analyze_security_event(event.event)

    return {
        "event": event.event,
        "analysis": analysis,
    }