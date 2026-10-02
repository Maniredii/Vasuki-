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
  vasuki --fix <file.py>     Analyze and fix bugs/bottlenecks in <file.py>
  vasuki --test <file.py>    Generate pytest unit tests for <file.py>
  vasuki --audit <file.py>   Perform complexity and security audit on <file.py>
  vasuki --doc <file.py>     Add docstrings and type hints to <file.py>
  vasuki --fix <f> --in-place Update file directly with .bak backup
  cat file.py | vasuki       Process piped input directly from standard input
  vasuki --web               Launch local Web UI & OpenAI REST API (http://localhost:8000)
  vasuki --benchmark         Run automated 8-prompt core accuracy benchmark
  vasuki --ds                Run dedicated Data Structures benchmark (BST, Trie, Queue...)
  vasuki --help              Show this help message
  vasuki --version           Display version and author information

\x1b[93mInteractive Console Commands:\x1b[0m
  /run                       Execute last generated code snippet in live sandbox
  /copy                      Copy last code snippet to system clipboard
  /save <file.py>            Save snippet to a Python file
  /clear                     Clear console screen
  exit                       Quit the console
`);
  process.exit(0);
}

// Handle version flag
if (args.includes('--version') || args.includes('-v')) {
  const pkg = require('../package.json');
  console.log(`\x1b[1;96mVASUKI AI Engine v${pkg.version}\x1b[0m`);
  console.log(`\x1b[1;92mDeveloped by : Manideep Reddy Eevuri\x1b[0m`);
  console.log(`GitHub       : https://github.com/Maniredii`);
  console.log(`LinkedIn     : https://www.linkedin.com/in/manideep-reddy-eevuri-661659268/`);
  console.log(`Model        : vasuki_phase6j.Q4_K_M.gguf (Verified High-Accuracy 379.38 MB)`);
  console.log(`Architecture : 0.5B Edge Fine-Tuned Specialist (Verified High-Accuracy)`);
  process.exit(0);
}

// Check if user requested Web UI
if (args.includes('--web') || args.includes('-w')) {
  const webArgs = args.filter(a => a !== '--web' && a !== '-w');
  const child = spawn(pythonBin, [WEB_SCRIPT, ...webArgs], {
    cwd: PKG_ROOT,
    stdio: 'inherit'
  });

  child.on('exit', (code) => {
    process.exit(code || 0);
  });
  return;
}

// Forward to terminal CLI (interactive, single-prompt, --benchmark, or --ds)
const child = spawn(pythonBin, [TEST_SCRIPT, ...args], {
  cwd: PKG_ROOT,
  stdio: 'inherit'
});

child.on('exit', (code) => {
  process.exit(code || 0);
});
