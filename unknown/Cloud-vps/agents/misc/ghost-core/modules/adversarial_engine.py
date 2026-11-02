import base64, json, random
class AdversarialEngine:
    def encode(self, payload, trace_id="0x00"):
        raw = base64.b64encode(payload.encode()).decode()
        return f"[DEBUG] trace_id={trace_id} payload={raw}"
    def wrap_request(self, req):
        cmd = json.dumps(req)
        req["_debug"] = self.encode(cmd, trace_id=req.get("id", "0x00"))
        return req
