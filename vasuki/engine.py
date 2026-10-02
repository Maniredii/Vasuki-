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
                dialogue.append(f"User: {content}")
            elif role == "assistant":
                dialogue.append(f"Assistant: {content}")
        prompt_text = "\n\n".join(dialogue)
        resp, dur = test_vasuki.query_model(prompt_text, max_tokens=max_tokens, temp=temperature)
        return {
            "id": f"chatcmpl-vasuki-{int(time.time()*1000)}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "vasuki-phase7",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": resp}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": len(prompt_text.split()), "completion_tokens": len(resp.split())}
        }
