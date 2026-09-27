/**
 * VASUKI-PY: Programmatic Node.js Interface
 * Usage:
 *   const { askVasuki, startWebUI } = require('vasuki-py');
 *   const response = await askVasuki("Write a function to check prime numbers");
 */

const { spawn, execSync } = require('child_process');
const path = require('path');

const PKG_ROOT = path.resolve(__dirname);
const TEST_SCRIPT = path.join(PKG_ROOT, 'test_vasuki.py');
const WEB_SCRIPT = path.join(PKG_ROOT, 'web_vasuki.py');

function getPythonBinary() {
  const candidates = ['python', 'python3', 'py'];
  for (const cmd of candidates) {
    try {
      execSync(`${cmd} --version`, { stdio: 'ignore' });
      return cmd;
    } catch (e) {
      // Continue search
    }
  }
  return null;
}

/**
 * Ask VASUKI a coding prompt programmatically in Node.js
 * @param {string} prompt - The coding task or algorithm request
 * @returns {Promise<{response: string, duration_seconds: number}>}
 */
function askVasuki(prompt) {
  return new Promise((resolve, reject) => {
    const py = getPythonBinary();
    if (!py) {
      return reject(new Error('Python 3 was not found in system PATH.'));
    }

    const proc = spawn(py, [TEST_SCRIPT, prompt], {
      cwd: PKG_ROOT
    });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', (chunk) => { stdout += chunk.toString(); });
    proc.stderr.on('data', (chunk) => { stderr += chunk.toString(); });

    proc.on('close', (code) => {
      if (code !== 0 && !stdout) {
        return reject(new Error(stderr || `VASUKI exited with code ${code}`));
      }
      resolve({
        response: stdout.trim(),
        raw: stdout
      });
    });
  });
}

/**
 * Starts the local VASUKI Web & Mobile server
 * @param {number} port - Default 8000
 */
function startWebUI(port = 8000) {
  const py = getPythonBinary();
  if (!py) {
    throw new Error('Python 3 was not found in system PATH.');
  }
  return spawn(py, [WEB_SCRIPT, String(port)], {
    cwd: PKG_ROOT,
    stdio: 'inherit'
  });
}

module.exports = {
  askVasuki,
  startWebUI
};
