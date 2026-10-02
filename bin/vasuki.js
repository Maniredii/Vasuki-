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
