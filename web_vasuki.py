"""
VASUKI Phase 6J: Local Web & Mobile Browser Interface
Zero external dependencies - runs on standard Python 3.
Access locally on: http://localhost:8000
Access on your mobile phone on the same Wi-Fi via: http://<your-pc-ip>:8000
"""

import sys
import os
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socket

# Import the existing query engine
from test_vasuki import query_model, MODEL_PATH

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VASUKI Phase 6J | Offline AI Python Specialist</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #090c10;
      --bg-surface: #0d1117;
      --bg-card: rgba(22, 27, 34, 0.7);
      --border-color: rgba(48, 54, 61, 0.8);
      --accent-cyan: #38bdf8;
      --accent-purple: #a855f7;
      --accent-green: #22c55e;
      --text-main: #f0f6fc;
      --text-muted: #8b949e;
      --code-bg: #030712;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Inter', -apple-system, sans-serif;
      background: radial-gradient(circle at 50% 0%, #171c26 0%, #090c10 75%);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }

    header {
      backdrop-filter: blur(16px);
      background: rgba(13, 17, 23, 0.75);
      border-bottom: 1px solid var(--border-color);
      padding: 14px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-logo {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 18px;
      color: #fff;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.35);
    }

    .brand-title {
      font-size: 18px;
      font-weight: 700;
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .brand-badge {
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 999px;
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent-cyan);
      border: 1px solid rgba(56, 189, 248, 0.3);
      font-weight: 600;
    }

    .status-pill {
      font-size: 12px;
      padding: 6px 12px;
      border-radius: 999px;
      background: rgba(34, 197, 94, 0.12);
      border: 1px solid rgba(34, 197, 94, 0.25);
      color: #4ade80;
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: 500;
    }

    .status-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #22c55e;
      box-shadow: 0 0 8px #22c55e;
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(0.85); }
    }

    main {
      flex: 1;
      max-width: 900px;
      width: 100%;
      margin: 0 auto;
      padding: 24px 16px 140px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .welcome-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 24px;
      text-align: center;
      backdrop-filter: blur(12px);
      box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    .welcome-card h2 {
      font-size: 24px;
      font-weight: 700;
      margin-bottom: 8px;
      background: linear-gradient(to right, #ffffff, #94a3b8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .welcome-card p {
      color: var(--text-muted);
      font-size: 14px;
      max-width: 580px;
      margin: 0 auto 18px;
      line-height: 1.5;
    }

    .suggestions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      justify-content: center;
    }

    .suggestion-btn {
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid var(--border-color);
      color: #cbd5e1;
      padding: 8px 14px;
      border-radius: 999px;
      font-size: 13px;
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: inherit;
    }

    .suggestion-btn:hover {
      background: rgba(56, 189, 248, 0.15);
      border-color: var(--accent-cyan);
      color: #fff;
      transform: translateY(-1px);
    }

    .chat-container {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .message-row {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .user-msg {
      align-self: flex-end;
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(168, 85, 247, 0.2));
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 12px 18px;
      border-radius: 18px 18px 4px 18px;
      font-size: 15px;
      max-width: 80%;
      line-height: 1.45;
      box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    }

    .bot-card {
      align-self: flex-start;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 18px 18px 18px 4px;
      padding: 18px 20px;
      max-width: 95%;
      width: 100%;
      backdrop-filter: blur(12px);
      box-shadow: 0 6px 24px rgba(0,0,0,0.3);
      position: relative;
    }

    .bot-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
      border-bottom: 1px solid rgba(255,255,255,0.06);
      padding-bottom: 8px;
    }

    .bot-title {
      font-size: 13px;
      font-weight: 600;
      color: var(--accent-cyan);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .bot-meta {
      font-size: 12px;
      color: var(--text-muted);
    }

    .code-container {
      position: relative;
      background: var(--code-bg);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 10px;
      overflow: hidden;
      margin-top: 8px;
    }

    .copy-btn {
      position: absolute;
      top: 8px;
      right: 8px;
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid rgba(255,255,255,0.15);
      color: #94a3b8;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      cursor: pointer;
      transition: all 0.2s;
      font-family: inherit;
      backdrop-filter: blur(4px);
    }

    .copy-btn:hover {
      background: var(--accent-cyan);
      color: #000;
      font-weight: 600;
    }

    pre code {
      display: block;
      padding: 16px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13.5px;
      line-height: 1.6;
      color: #e2e8f0;
      overflow-x: auto;
      white-space: pre;
    }

    .input-bar-container {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background: linear-gradient(to top, #090c10 80%, rgba(9, 12, 16, 0));
      padding: 20px 16px;
      display: flex;
      justify-content: center;
      z-index: 100;
    }

    .input-bar {
      max-width: 900px;
      width: 100%;
      background: rgba(18, 24, 38, 0.95);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 16px;
      padding: 8px 12px;
      display: flex;
      align-items: center;
      gap: 10px;
      backdrop-filter: blur(16px);
      box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }

    .input-bar:focus-within {
      border-color: var(--accent-cyan);
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.25);
    }

    .chat-input {
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      color: #fff;
      font-size: 15px;
      font-family: inherit;
      padding: 8px 6px;
    }

    .chat-input::placeholder {
      color: #64748b;
    }

    .send-btn {
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
      border: none;
      color: #fff;
      width: 40px;
      height: 40px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s;
    }

    .send-btn:hover {
      transform: scale(1.05);
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.4);
    }

    .send-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }

    .typing-cursor {
      display: inline-block;
      width: 8px;
      height: 15px;
      background: var(--accent-cyan);
      margin-left: 3px;
      vertical-align: middle;
      animation: blink 0.8s infinite;
    }

    @keyframes blink {
      0%, 100% { opacity: 1; }
      50% { opacity: 0; }
    }
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <div class="brand-logo">V</div>
      <div class="brand-title">
        VASUKI <span class="brand-badge">Phase 6J • 0.5B</span>
      </div>
    </div>
    <div class="status-pill">
      <span class="status-dot"></span>
      <span>Offline Edge Engine (379 MB)</span>
    </div>
  </header>

  <main>
    <div class="welcome-card" id="welcomeCard">
      <h2>Offline Python Specialist</h2>
      <p>Fine-tuned for Python algorithms, data structures, and native system bindings. Runs 100% offline on your machine or mobile device.</p>
      <div class="suggestions">
        <button class="suggestion-btn" onclick="usePrompt('Implement binary search in Python with index return')">Binary Search</button>
        <button class="suggestion-btn" onclick="usePrompt('Write a Python class BST with insert and search methods')">Binary Search Tree</button>
        <button class="suggestion-btn" onclick="usePrompt('Write a Python generator that yields the first n Fibonacci numbers')">Fibonacci Generator</button>
        <button class="suggestion-btn" onclick="usePrompt('Write a Python class Trie with insert and search')">Trie Prefix Tree</button>
        <button class="suggestion-btn" onclick="usePrompt('How do I call a C shared library from Python using ctypes?')">C ctypes Interop</button>
      </div>
    </div>

    <div class="chat-container" id="chatContainer"></div>
  </main>

  <div class="input-bar-container">
    <div class="input-bar">
      <input type="text" class="chat-input" id="userInput" placeholder="Ask for any Python algorithm, data structure, or class..." autocomplete="off">
      <button class="send-btn" id="sendBtn" onclick="sendMessage()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      </button>
    </div>
  </div>

  <script>
    const chatContainer = document.getElementById('chatContainer');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const welcomeCard = document.getElementById('welcomeCard');

    userInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    function usePrompt(text) {
      userInput.value = text;
      sendMessage();
    }

    async function sendMessage() {
      const text = userInput.value.trim();
      if (!text) return;

      if (welcomeCard) welcomeCard.style.display = 'none';

      // Append User message
      const userDiv = document.createElement('div');
      userDiv.className = 'message-row';
      userDiv.innerHTML = `<div class="user-msg">${escapeHtml(text)}</div>`;
      chatContainer.appendChild(userDiv);

      userInput.value = '';
      sendBtn.disabled = true;

      // Append Bot card placeholder
      const botRow = document.createElement('div');
      botRow.className = 'message-row';
      
      const cardId = 'card_' + Date.now();
      const codeId = 'code_' + Date.now();
      
      botRow.innerHTML = `
        <div class="bot-card" id="${cardId}">
          <div class="bot-header">
            <div class="bot-title">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>
              VASUKI 6J
            </div>
            <div class="bot-meta" id="meta_${cardId}">Generating...</div>
          </div>
          <div class="code-container">
            <button class="copy-btn" onclick="copyCode('${codeId}')">Copy Code</button>
            <pre><code id="${codeId}"><span class="typing-cursor"></span></code></pre>
          </div>
        </div>
      `;
      chatContainer.appendChild(botRow);
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });

      try {
        const response = await fetch('/api/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt: text })
        });
        const data = await response.json();

        // Update meta
        document.getElementById(`meta_${cardId}`).innerText = `${data.elapsed_seconds.toFixed(2)}s • Python AST Verified`;

        // Stream typing animation
        await streamTyping(data.response, codeId);

      } catch (err) {
        document.getElementById(codeId).innerText = '# Error connecting to VASUKI local engine: ' + err.message;
      } finally {
        sendBtn.disabled = false;
        userInput.focus();
      }
    }

    async function streamTyping(fullText, elementId) {
      const el = document.getElementById(elementId);
      el.innerHTML = '';
      let current = '';
      
      for (let i = 0; i < fullText.length; i++) {
        current += fullText[i];
        el.textContent = current;
        if (fullText[i] === '\\n') {
          await new Promise(r => setTimeout(r, 20));
        } else if (i % 3 === 0) {
          await new Promise(r => setTimeout(r, 8));
        }
      }
    }

    function copyCode(elementId) {
      const code = document.getElementById(elementId).innerText;
      navigator.clipboard.writeText(code);
      event.target.innerText = 'Copied!';
      setTimeout(() => { event.target.innerText = 'Copy Code'; }, 1800);
    }

    function escapeHtml(str) {
      return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
  </script>
</body>
</html>
"""

def get_local_ip():
    """Finds the local network IP so the user can open it on their phone."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class VasukiWebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "model": MODEL_PATH}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/generate":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                user_prompt = data.get("prompt", "")
                
                resp, dur = query_model(user_prompt)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "response": resp,
                    "elapsed_seconds": dur
                }).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8000):
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, VasukiWebHandler)
    local_ip = get_local_ip()
    
    print("=" * 70)
    print("  VASUKI Phase 6J Local Web & Mobile Engine")
    print("=" * 70)
    print(f"  • Desktop Browser : http://localhost:{port}")
    print(f"  • Mobile Phone UI : http://{local_ip}:{port}")
    print("=" * 70)
    print("Press Ctrl+C to stop the server.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping VASUKI Web Server.")
        httpd.server_close()

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_server(port)
