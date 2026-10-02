#!/usr/bin/env node

/**
 * VASUKI CLI (npm package binary)
 * Lightweight bridge to the offline 0.5B Python specialist engine.
 */

const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const PKG_ROOT = path.resolve(__dirname, '..');
const TEST_SCRIPT = path.join(PKG_ROOT, 'test_vasuki.py');
const WEB_SCRIPT = path.join(PKG_ROOT, 'web_vasuki.py');

// Find a working Python binary on the system
function getPythonBinary() {
  const candidates = ['python', 'python3', 'py'];
  for (const cmd of candidates) {
    try {
      execSync(`${cmd} --version`, { stdio: 'ignore' });
      return cmd;
    } catch (e) {
      // Continue checking next candidate
    }
  }
  return null;
}

const pythonBin = getPythonBinary();
if (!pythonBin) {
  console.error('\x1b[91m[Error] Python 3 was not found in your system PATH.\x1b[0m');
  console.error('Please install Python 3 (https://www.python.org/) to run VASUKI.');
  process.exit(1);
}

const args = process.argv.slice(2);

// Handle help flag
if (args.includes('--help') || args.includes('-h')) {
  console.log(`
\x1b[1;96m========================================================================\x1b[0m
  \x1b[1;97mVASUKI Phase 7\x1b[0m \x1b[90m•\x1b[0m \x1b[96m0.5B Edge Python Reasoning AI Engine\x1b[0m
  \x1b[1;92mDeveloped by : Manideep Reddy Eevuri\x1b[0m
  \x1b[94mGitHub       :\x1b[0m https://github.com/Maniredii
  \x1b[94mLinkedIn     :\x1b[0m https://www.linkedin.com/in/manideep-reddy-eevuri-661659268/
\x1b[1;96m========================================================================\x1b[0m

\x1b[93mUsage:\x1b[0m
  vasuki                     Start interactive live console (with typing animation)
  vasuki "<prompt>"          Ask a specific Python question / task
  vasuki --web               Launch local Web UI & Mobile server (http://localhost:8000)
  vasuki --benchmark         Run automated 8-prompt core accuracy benchmark
  vasuki --ds                Run dedicated Data Structures benchmark (BST, Trie, Queue...)
  vasuki --help              Show this help message
  vasuki --version           Display version and author information

\x1b[93mInteractive Console Commands:\x1b[0m
  /run                       Execute last generated code snippet in sandbox
  /copy                      Copy last code snippet to system clipboard
