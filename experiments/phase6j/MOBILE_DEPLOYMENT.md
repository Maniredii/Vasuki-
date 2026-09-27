# VASUKI Phase 6J — Mobile Model Deployment Guide

## 📱 How to Run on Mobile (Android & iOS)

### Option 1: PocketPal AI (Easiest — Android & iOS)
1. Download PocketPal AI from Google Play Store or Apple App Store.
2. Transfer the .gguf file (e.g. vasuki_phase6j-Q4_K_M.gguf) to your phone's storage.
3. Open PocketPal AI -> Models -> Add Local Model -> Select the .gguf file.
4. Enjoy your offline, specialized Python assistant on your phone!

### Option 2: Termux / llama.cpp (Android Power Users)
```bash
pkg install clang cmake git
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make
./llama-cli -m vasuki_phase6j-Q4_K_M.gguf -p "### Instruction:\nExplain list comprehensions in Python.\n\n### Response:\n"
```
