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

