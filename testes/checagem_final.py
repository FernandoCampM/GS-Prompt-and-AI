import json, re, zipfile, os
E = "entrega"
arquivos = ["1_Notebook_GS2026_2.ipynb", "2_dados_servico.json", "3_prompts_kit.md",
            "4_README.md", "5_certificacao.txt", "6_Chat_Log.txt"]
ok = True
def check(cond, msg):
    global ok; ok &= bool(cond); print("✅" if cond else "❌", msg)

check(all(os.path.exists(f"{E}/{a}") for a in arquivos), "os 6 arquivos existem")
nb = json.load(open(f"{E}/1_Notebook_GS2026_2.ipynb", encoding="utf-8"))
texto_nb = json.dumps(nb, ensure_ascii=False)
titulos = [l for c in nb["cells"] if c["cell_type"] == "markdown" for l in "".join(c["source"]).splitlines() if re.match(r"^## \d\. ", l)]
check(titulos == ["## 0. Metadados", "## 1. Coleta e estruturação dos dados", "## 2. Enriquecimento com LLM",
                  "## 3. Validação e governança", "## 4. Construção do system prompt", "## 5. Testes e avaliação",
                  "## 6. Uso e limites da solução", "## 7. Conclusão"], "títulos das seções exatos")
codigo_nb = "".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")
check(not re.search(r"\bclass\s+\w+\s*[:(]", codigo_nb), "sem class")
todos = texto_nb + "".join(open(f"{E}/{a}", encoding="utf-8").read() for a in arquivos[1:])
check(not re.search(r"Bearer\s+[A-Za-z0-9_\-\.]{12,}|OLLAMA_API_KEY\s*=\s*['\"][^'\"]{8,}", todos), "nenhuma chave escrita")
check(any(c.get("outputs") for c in nb["cells"] if c["cell_type"] == "code"), "notebook salvo COM saídas da execução real")
check("(None," not in codigo_nb, "matriz humana preenchida (sem None)")
dados = json.load(open(f"{E}/2_dados_servico.json", encoding="utf-8"))
check(len(dados) >= 10 and len({d['id'] for d in dados}) == len(dados), ">= 10 registros, ids únicos")
check(sum(d["status"] != "ativo" for d in dados) >= 2, ">= 2 status fora do normal")
check(all(isinstance(d["acessivel"], bool) for d in dados), "acessivel booleano")
cert = open(f"{E}/5_certificacao.txt", encoding="utf-8").read()
check("__/__" not in cert and "(colar" not in cert, "certificação preenchida (saída real + links)")
check("| P1 | | | |" not in open(f"{E}/3_prompts_kit.md", encoding="utf-8").read(), "tabela de iterações do kit preenchida")
check("[completar" not in open(f"{E}/6_Chat_Log.txt", encoding="utf-8").read(), "chat log completado")
check("Substituir pelos prints" not in open(f"{E}/4_README.md", encoding="utf-8").read(), "prints no README")
check("(ajustar ao que cada um fez" not in texto_nb, "divisão de tarefas confirmada")
check("reescrevam com as palavras de vocês" not in texto_nb, "conclusão reescrita pela dupla")
if ok:
    with zipfile.ZipFile("GS2026_2_1CCPS_AcessaMetro.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for a in arquivos:
            z.write(f"{E}/{a}", arcname=a)   # sem pasta dentro do zip
    print("\n📦 GS2026_2_1CCPS_AcessaMetro.zip gerado")
else:
    print("\n⛔ Corrija os itens ❌ antes de gerar o zip.")
