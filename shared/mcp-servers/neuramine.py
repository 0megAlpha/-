from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio
app=Server("neuramine")
@app.tool()
def store(key:str,value:str)->str:return f"stored:{key}"
@app.tool()
def recall(key:str)->str:return ""
async def main():
    async with stdio_server(app)as(r,w):await app.run(r,w,app.create_initialization_options())
if __name__=="__main__":asyncio.run(main())
