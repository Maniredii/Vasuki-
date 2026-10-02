"""
VASUKI: Offline Python Reasoning AI Engine
Developed by: Manideep Reddy Eevuri
GitHub: https://github.com/Maniredii
LinkedIn: https://www.linkedin.com/in/manideep-reddy-eevuri-661659268/
"""

__version__ = "1.1.0"
__author__ = "Manideep Reddy Eevuri"

from .engine import VasukiEngine, query_model, resolve_model_path
from .downloader import ensure_model_downloaded

_default_engine = None

def get_engine():
    global _default_engine
    if _default_engine is None:
        _default_engine = VasukiEngine()
    return _default_engine

def generate(prompt: str, max_tokens: int = 350, temperature: float = 0.2) -> str:
    """Generate Python code or reasoning response for a given prompt."""
    return get_engine().generate(prompt, max_tokens=max_tokens, temperature=temperature)

def ask(prompt: str, **kwargs) -> str:
    """Alias for generate()."""
    return generate(prompt, **kwargs)

def chat(messages: list, **kwargs) -> dict:
    """Generate a chat completion given an OpenAI-style list of messages."""
    return get_engine().chat(messages, **kwargs)

def start_server(port: int = 8000):
    """Launch the local Web UI and OpenAI-compatible REST server."""
    import web_vasuki
    web_vasuki.run_server(port=port)
