const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
class SandboxRunner {
  constructor() { this.workspace = '/opt/opencode-sandbox/workspace'; this.image = 'opencode-sandbox:latest'; }
  executeCode(code, language = 'python') {
    const f = path.join(this.workspace, `test_${Date.now()}.${language === 'python' ? 'py' : 'js'}`);
    fs.writeFileSync(f, code);
    try {
      const out = execSync(`docker run --rm -v ${this.workspace}:/workspace ${this.image} ${language === 'python' ? 'python' : 'node'} /workspace/${path.basename(f)}`, { encoding: 'utf-8', timeout: 120000 });
      fs.unlinkSync(f); return { success: true, output: out };
    } catch (e) { fs.unlinkSync(f); return { success: false, error: e.message }; }
  }
  runTests(p) {
    try { return { success: true, output: execSync(`docker run --rm -v ${this.workspace}:/workspace ${this.image} npx jest /workspace/${p}`, { encoding: 'utf-8', timeout: 120000 }) }; }
    catch (e) { return { success: false, error: e.message }; }
  }
}
module.exports = SandboxRunner;
