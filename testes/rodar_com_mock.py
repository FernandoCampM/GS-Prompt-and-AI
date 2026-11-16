"""Executa todas as células de código do notebook com um LLM SIMULADO (sem rede, sem chave).
Serve só para provar que o Run all não quebra. Não substitui a execução real no Colab.

Uso (a partir da pasta do projeto):
    python testes/rodar_com_mock.py                      # mock: algumas respostas válidas, outras inválidas
    MOCK_NOKEY=1 python testes/rodar_com_mock.py         # simula Colab sem chave -> tudo vai para o fallback
    MOCK_FAIL_ASSIST=1 python testes/rodar_com_mock.py   # simula a nuvem caindo no meio
Os arquivos gerados (2_dados_servico.json, trilha_auditoria.json) vão para testes/saida/.
"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "mocks"))
nb_path = os.path.join(AQUI, "..", "entrega", "1_Notebook_GS2026_2.ipynb")
nb = json.load(open(nb_path, encoding="utf-8"))
codigo = []
for c in nb["cells"]:
    if c["cell_type"] == "code":
        linhas = "".join(c["source"]).splitlines()
        codigo.append("\n".join(l for l in linhas if not l.lstrip().startswith(("!", "%"))))
saida = os.path.join(AQUI, "saida")
os.makedirs(saida, exist_ok=True)
os.chdir(saida)
exec(compile("\n\n".join(codigo), "notebook", "exec"), {"__name__": "__main__"})
print("\nOK: o notebook rodou do início ao fim com o mock.")
