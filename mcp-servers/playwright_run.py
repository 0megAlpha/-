from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio,os
app=Server("playwright")
CHROMIUM="/data/data/com.termux/files/usr/bin/chromium"
@app.tool()
def run_script(script:str)->str:
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright()as p:
            br=p.chromium.launch(headless=True,executable_path=CHROMIUM if os.path.exists(CHROMIUM)else None,args=["--no-sandbox","--disable-dev-shm-usage"])
            ctx=br.new_context(user_agent="Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36");pg=ctx.new_page()
            ns={"page":pg,"context":ctx,"browser":br};exec(script,ns);br.close()
            return str(ns.get("_result","ok"))[:2000]
    except Exception as e:return f"ERR:{e}"
async def main():
    async with stdio_server(app)as(r,w):await app.run(r,w,app.create_initialization_options())
if __name__=="__main__":asyncio.run(main())
