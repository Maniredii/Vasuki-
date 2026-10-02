import os
import sys
import time
import test_vasuki

class VasukiEngine:
    """
    High-level Python wrapper around the offline VASUKI Phase 7 Reasoning Engine.
    """
    def __init__(self, model_path: str = None):
        self.model_path = model_path or test_vasuki.MODEL_PATH

    def generate(self, prompt: str, max_tokens: int = 350, temperature: float = 0.2) -> str:
        resp, _ = test_vasuki.query_model(prompt, max_tokens=max_tokens, temp=temperature)
        return resp

    def chat(self, messages: list, max_tokens: int = 350, temperature: float = 0.2) -> dict:
        dialogue = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role == "system":
                dialogue.append(f"Context: {content}")
            elif role == "user":
