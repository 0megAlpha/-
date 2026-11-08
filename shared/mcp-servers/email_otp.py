from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio,requests,re,random
app=Server("email_otp")
@app.tool()
def create_mailbox()->str:
    u=f"m{random.randint(100000,999999)}";pwd="Zz13590"
    r=requests.post("https://api.mail.tm/accounts",json={"address":f"{u}@mail.tm","password":pwd},timeout=15)
    return f"{r.json()['address']}:{pwd}" if r.status_code in(200,201) else "FAILED"
@app.tool()
def fetch_otp(email:str,password:str)->str:
    tr=requests.post("https://api.mail.tm/token",json={"address":email,"password":password},timeout=10)
    if tr.status_code!=200:return ""
    tok=tr.json().get("token");mr=requests.get("https://api.mail.tm/messages",headers={"Authorization":f"Bearer {tok}"},timeout=10)
    for msg in mr.json().get("hydra:member",[]):
        det=requests.get(f"https://api.mail.tm/messages/{msg['id']}",headers={"Authorization":f"Bearer {tok}"},timeout=10)
        body=(det.json().get("text")or"")+str(det.json().get("html")or"")
        codes=re.findall(r'\b\d{4,8}\b',body)
        if codes:return codes[0]
    return ""
async def main():
    async with stdio_server(app)as(r,w):await app.run(r,w,app.create_initialization_options())
if __name__=="__main__":asyncio.run(main())
