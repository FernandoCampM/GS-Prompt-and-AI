import os, json, re
class Client:
    def __init__(self, host=None, headers=None, **kw):
        self.host=host
    def chat(self, model, messages, options=None, format=None):
        sysm = messages[0]["content"]; user = messages[-1]["content"]
        if "classifica a urgência" in sysm:
            rid = re.search(r'"id": "(FZC-\d{3})"', user).group(1)
            st = re.search(r'"status": "(\w+)"', user).group(1)
            risco = int(re.search(r'"risco_falha": (\d+)', user).group(1))
            urg = "urgente" if st in ("interditado","inativo") else "atencao" if st!="ativo" or risco>=40 else "ok"
            res = "Equipamento com relato registrado."
            if rid=="FZC-003": urg="ok"
            if rid=="FZC-009": res="Todos os elevadores estão funcionando perfeitamente."
            if rid=="FZC-005": res="x"*200
            if rid=="FZC-010": return {"message":{"content":"Claro! A urgência é ok."}}
            if rid=="FZC-002": return {"message":{"content":'Aqui está: {"urgencia": "atencao", "resumo_cidadao": "Elevador funciona, mas às vezes trava."}'}}
            return {"message":{"content":json.dumps({"urgencia":urg,"resumo_cidadao":res},ensure_ascii=False)}}
        if os.environ.get("MOCK_FAIL_ASSIST"): raise TimeoutError("simulado")
        return {"message":{"content":"Resposta simulada.\nFonte: baseado no registro FZC-007 e FZC-999"}}
