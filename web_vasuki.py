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
  <title>VASUKI Phase 7 | Offline AI Python Reasoning Specialist</title>
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

    .brand-subtitle {
      font-size: 11.5px;
      color: var(--text-muted);
      margin-top: 1px;
    }

    .brand-subtitle strong {
      color: #38bdf8;
      font-weight: 600;
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .social-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 12px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 500;
      text-decoration: none;
      transition: all 0.2s ease;
      border: 1px solid var(--border-color);
      color: var(--text-main);
      background: rgba(22, 27, 34, 0.8);
    }

    .social-btn:hover {
      border-color: var(--accent-cyan);
      color: #fff;
      transform: translateY(-1px);
    }

    .social-btn.linkedin-btn:hover {
      border-color: #0a66c2;
      box-shadow: 0 0 10px rgba(10, 102, 194, 0.35);
    }

    .social-btn.github-btn:hover {
      border-color: #f0f6fc;
      box-shadow: 0 0 10px rgba(240, 246, 252, 0.25);
    }

    .author-card {
      margin-top: 16px;
      margin-bottom: 8px;
      padding: 10px 18px;
      background: rgba(13, 17, 23, 0.7);
      border: 1px solid rgba(56, 189, 248, 0.25);
      border-radius: 12px;
      display: inline-flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
    }

    .author-meta {
      font-size: 13px;
      color: var(--text-main);
      font-weight: 500;
    }

    .author-meta strong {
      color: #4ade80;
    }

    .author-links {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 12px;
    }

    .author-links a {
      color: var(--accent-cyan);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: color 0.2s;
    }

    .author-links a:hover {
      text-decoration: underline;
      color: #7dd3fc;
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
