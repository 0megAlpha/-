from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio
app=Server("proxy_rotate")
@app.tool()
def info()->str:return "proxy_rotate ready"
async def main():
    async with stdio_server(app)as(r,w):await app.run(r,w,app.create_initialization_options())
if __name__=="__main__":asyncio.run(main())
