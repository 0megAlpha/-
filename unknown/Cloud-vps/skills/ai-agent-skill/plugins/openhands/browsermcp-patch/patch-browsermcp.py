from pathlib import Path
p = Path("/opt/browsermcp/node_modules/@browsermcp/mcp/dist/index.js")
s = p.read_text()
old_kill = 'execSync(`lsof -ti:${port} | xargs kill -9`);'
new_kill = '''const pids = execSync(`lsof -ti:${port} || true`, { encoding: "utf8" }).trim().split(String.fromCharCode(10)).filter(Boolean);
      if (pids.length > 0) execSync(`kill -9 ${pids.join(" ")}`);'''
old_close = '''  server.close = async () => {
    await server.close();
    await wss.close();
    await context.close();
  };'''
new_close = '''  const originalClose = server.close.bind(server);
  server.close = async () => {
    await originalClose();
    await wss.close();
    await context.close();
  };'''
assert old_kill in s, "port-kill pattern not found"
assert old_close in s, "recursive close pattern not found"
s = s.replace(old_kill, new_kill, 1).replace(old_close, new_close, 1)
p.write_text(s)
print("patched_port_kill=", old_kill in p.read_text(), "patched_close=", "await originalClose();" in p.read_text())
