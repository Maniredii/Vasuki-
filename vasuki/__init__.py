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

def generate(prompt: str, max_tokens: int = 350, temperature: float = 0.2) 