import os
import sys
import urllib.request

DEFAULT_MODEL_NAME = "vasuki_phase7.Q4_K_M.gguf"
HF_REPO_URL = "https://huggingface.co/Maniredii/Vasuki-Phase7/resolve/main/vasuki_phase7.Q4_K_M.gguf"

def get_target_model_path():
    home_dir = os.path.expanduser("~")
    models_dir = os.path.join(home_dir, ".vasuki", "models")
    os.makedirs(models_dir, exist_ok=True)
    return os.path.join(models_dir, DEFAULT_MODEL_NAME)

def ensure_model_downloaded():
    local_path = get_target_model_path()
    if os.path.exists(local_path) and os.path.getsize(local_path) > 100_000_000:
