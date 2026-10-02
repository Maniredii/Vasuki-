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
        return local_path
    
    workspace_cand = os.path.join(os.getcwd(), DEFAULT_MODEL_NAME)
    if os.path.exists(workspace_cand) and os.path.getsize(workspace_cand) > 100_000_000:
        return workspace_cand

    print(f"[*] VASUKI model not found locally. Preparing to download from Hugging Face...")
    print(f"[*] Target destination: {local_path}")
    return local_path
