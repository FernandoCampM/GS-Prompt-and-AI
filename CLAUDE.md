# CLAUDE.md — Acessa Metrô · GS2026.2 (Prompt and Artificial Intelligence)

Você está ajudando a dupla **Fernando Campos Garnica Mota (RM 567451)** e **André da Silva Pinto (RM 559038)**, turma **1CCPS**, a terminar a Global Solution 2026.2 da disciplina *Prompt and Artificial Intelligence* (Prof. Jorge Luiz Gomes, FIAP).

**Prazo: 19/11/2026, 23h59, no Portal FIAP.** Entrega: **um `.zip` com exatamente 6 arquivos, sem pasta dentro**, chamado `GS2026_2_1CCPS_AcessaMetro.zip`.

Responda sempre em **português**. Para explicar conceitos, use diagramas ASCII e linguagem simples.

> **Comece toda sessão assim:** leia a seção 9 (**Diário**) para saber onde a dupla parou, e a seção 4 (**Tarefas**) para saber o que falta. O Fernando troca de PC: se for um PC novo, faça antes a seção 5 (**Preparar o PC**).

## ▶ Próxima sessão: comece aqui (atualizado em 18/11/2026)

**Feito:** tarefa 0 (divisão de tarefas e modelo); plano B ativo (`llama3.2:1b` no Colab, sem chave, com timeout de 120 s e limite de 512 tokens); resumo das sessões no chat log; script de apoio `testes/comparar_respostas.py`.

**Faça nesta ordem:**
1. `git pull` e, se o PC for novo, a seção 5 (`py -3 -m pip install pandas`).
2. **Tarefa A:** pergunte se a dupla já rodou o notebook novo no Colab. Se não, oriente: upload de `entrega/1_Notebook_GS2026_2.ipynb` → `Alterar o tipo de ambiente → GPU T4` → `Executar tudo` (não precisa de chave) → `Arquivo → Fazer download → .ipynb`. Peça o caminho do arquivo baixado e verifique **antes** de copiar para `entrega/`: sem erros, chave ausente, `LLM disponível: True`, e na certificação a maioria das 27 chamadas "com sucesso". Se ainda cair tudo no fallback ou travar, investigue a saída da célula do cliente (Seção 1) e da célula 7 (Seção 2).
3. **Tarefa B:** com o notebook bom em `entrega/`, rode `PYTHONIOENCODING=utf-8 py -3 testes/comparar_respostas.py entrega/1_Notebook_GS2026_2.ipynb` e mostre à dupla `testes/saida/comparacao_P1_P5.md`, pergunta por pergunta. **As notas são da dupla** (regra 2). Depois, escreva em `NOTAS_HUMANAS` e peça para rodar de novo a 5.2 e a certificação no Colab.
4. **Tarefas C, D, E, F, G (resto) e H**, como na seção 4. Para a D (prompt e tese), entreviste a dupla; não escreva por ela (regra 3). Na G, falta só o item `[completar: …]`, que a dupla responde.
5. Prazo: **19/11/2026, 23h59**. Se o tempo apertar, priorize A → B → E → H. Sem saídas reais e sem notas humanas, o zip não passa na checagem.

---

## 1. Contexto do projeto

- **Frente C — Acessibilidade.** Ideia do Fernando: monitorar a "saúde" de elevadores, escadas rolantes e esteiras rolantes do metrô de SP, como os *health checks* do Zabbix. O objetivo é manter o funcionamento o mais perto possível de 100% e mostrar ao técnico qual equipamento está mais perto de quebrar, para ele saber o que priorizar.
- **Dois públicos, uma base:**
  ```
  telemetria simulada (estilo Zabbix) ─► risco_falha (regra) ─► LLM: urgente/atencao/ok ─► fila do TÉCNICO
                     │
                     └──────────────────► assistente "Acessa Metrô" ─► CIDADÃO (funciona? alternativa acessível?)
  ```
- **Dados:** 12 equipamentos em 7 estações reais (Sé, Paraíso, Consolação, Tatuapé, Santana, Luz e Jabaquara). Status, números e relatos são **fictícios**. São 13 registros brutos, um duplicado de propósito, o que dá 12 válidos, 4 deles fora do normal (FZC-003, 005, 007 e 011).
- **Perto de quebrar (ativos com risco alto):** FZC-009 (risco 76) e FZC-002 (risco 49). Eles mostram a ideia central: um equipamento que ainda funciona, mas deve ir para a frente da fila.
- `acessivel` = **"atende quem usa cadeira de rodas"**. Elevador e esteira plana são `true`; escada rolante é `false`.
- **Fórmula do risco:** `falhas_30d × 10 + (100 − disponibilidade_30d) × 0,5 + 15 se a última manutenção foi há mais de 120 dias`, com máximo de 100. `DATA_REFERENCIA = 2026-11-16`.
- O relato do **FZC-009** traz uma *prompt injection* **de propósito**. Não "corrija": é o teste de robustez.
- **Canal oficial:** Central de Informações do Metrô, 0800 770 7722 (todos os dias, das 5h à meia-noite), ou app Metrô Conecta.
- **Modelo (atual): `llama3.2:1b` rodando no Colab via Ollama (`USAR_OLLAMA_LOCAL = True`), sem chave.** O código da nuvem (`gpt-oss:20b`, chave em `userdata.get('OLLAMA_API_KEY')`) continua no notebook para quem mudar o flag para `False`. Toda chamada tem `TEMPO_LIMITE_S = 120` e `MAX_TOKENS = 512`. Decisão da dupla em 16/11: manter o `gpt-oss:20b`. **Em 17/11 a nuvem pediu crédito (0 de 27 chamadas) e a dupla ativou o plano B: `USAR_OLLAMA_LOCAL = True`, com `llama3.2:1b` rodando no Colab e sem chave.** O mock força o ramo da nuvem; `MOCK_LOCAL=1` testa o ramo local, que fora do Colab cai no fallback sem quebrar.
- **Origem:** o rascunho dos 6 arquivos foi gerado no claude.ai em 16/11/2026 e trazido para cá. Ele foi revisado no Claude Code em 16/11 e roda com o mock.
- O enunciado oficial está em `Briefing_GS2026_2.pdf`. **Em caso de dúvida, o briefing manda.**

## 2. Mapa de arquivos

```
GSPROMPTANDAI/                     ← raiz do projeto (no PC do Fernando: Desktop\GSPROMPTANDAI)
├── CLAUDE.md                      ← este arquivo (NÃO vai no zip)
├── Briefing_GS2026_2.pdf          ← enunciado oficial (NÃO vai no zip)
├── entrega/                       ← os 6 arquivos que vão no zip, e SÓ eles
│   ├── 1_Notebook_GS2026_2.ipynb
│   ├── 2_dados_servico.json       (gerado pela Seção 1 do notebook; não editar à mão)
│   ├── 3_prompts_kit.md
│   ├── 4_README.md
│   ├── 5_certificacao.txt
│   └── 6_Chat_Log.txt
├── testes/
│   ├── rodar_com_mock.py          ← roda todas as células com um LLM simulado
│   ├── comparar_respostas.py      ← monta P1–P5 (v1 × v2) de um notebook executado, para as notas da dupla
│   ├── checagem_final.py          ← checagem da seção 7 + gera o zip
│   ├── mocks/                     ← falsos ollama / google.colab / IPython
│   └── saida/                     ← gerado pelo teste (pode apagar; NÃO vai no zip)
└── GS2026_2_1CCPS_AcessaMetro.zip ← só aparece depois da checagem final (seção 7)
```

## 3. Formato que o professor exige (não negociável)

| Item | Regra |
|---|---|
| Zip | `GS2026_2_1CCPS_AcessaMetro.zip`, com os 6 arquivos **na raiz** (sem pasta dentro) |
| Nomes | exatamente `1_Notebook_GS2026_2.ipynb`, `2_dados_servico.json`, `3_prompts_kit.md`, `4_README.md`, `5_certificacao.txt`, `6_Chat_Log.txt` |
| Notebook | roda com `Runtime → Run all` no Colab, sem API paga. Se não rodar: **−1,5** |
| Títulos | `## 0. Metadados`, `## 1. Coleta e estruturação dos dados`, `## 2. Enriquecimento com LLM`, `## 3. Validação e governança`, `## 4. Construção do system prompt`, `## 5. Testes e avaliação`, `## 6. Uso e limites da solução`, `## 7. Conclusão` (exatos) |
| Chave | `OLLAMA_API_KEY` **nunca** aparece escrita. Se aparecer, o notebook não é corrigido |
| Dados | dupla: **≥ 10 registros**, ≥ 2 fora do normal, ids `FZC-000` únicos, `acessivel` booleano |
| Prompt | os 7 elementos (persona/escopo, fonte da verdade, dados ausentes, tom, anti-injection, 1 few-shot, formato ≤ 4 linhas + `baseado no registro FZC-00X`) e a frase literal *"se não estiver nos dados, diga que não há informação e indique o canal oficial"* |
| Testes | 5 perguntas × 2 versões (v1 simples, v2 enriquecida) e matriz com **notas humanas** |
| Seção 6 | bloco JSON com `versao, frente, dados, system_prompt, few_shot, perguntas_de_teste, limitacoes` |
| Conclusão | até **10 linhas**, com a tese da dupla |
| Código | **nada de `class`**: só listas, dicionários e funções (regra do 1º semestre) |

## 4. Tarefas que faltam

Faça na ordem. Quando terminar uma, marque `[x]` aqui **e** escreva uma linha no Diário (seção 9).

### [x] 0. Decisões pendentes da dupla
- [x] Qual modelo usar? Em 16/11 a dupla decidiu manter o `gpt-oss:20b` (Ollama Cloud). **Em 17/11, como a nuvem pediu crédito, a dupla trocou para o plano B: `llama3.2:1b` no próprio Colab.**
- [x] Confirmar a **divisão de tarefas** da Seção 0. **Decidido em 16/11** (ver Diário).

### [x] A. Executar o notebook com o modelo de verdade
- **Caminho principal (Colab, plano B):** a dupla abre o `.ipynb` no Colab, escolhe **GPU T4** (`Alterar o tipo de ambiente`), roda `Runtime → Run all` (sem chave) e baixa o notebook **com as saídas** (`Arquivo → Baixar → .ipynb`). Esse arquivo substitui `entrega/1_Notebook_GS2026_2.ipynb`, depois de verificado. Histórico: 1ª execução (17/11, nuvem) caiu toda no fallback por falta de crédito; 2ª (17/11, local em CPU) travou na célula 7, o que motivou o timeout.
- **Caminho local (opcional):** fora do Colab, a célula do cliente lê a variável de ambiente `OLLAMA_API_KEY`. Peça para a dupla definir a chave no próprio terminal. **Nunca peça para colarem a chave no chat.** Depois rode:
  ```bash
  py -3 -m pip install ollama pandas nbconvert ipykernel
  py -3 -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=900 entrega/1_Notebook_GS2026_2.ipynb
  ```
  Depois, confira nas saídas que a chave **não** foi impressa.
- **Se a nuvem pedir crédito:** troque para `USAR_OLLAMA_LOCAL = True` (só funciona no Colab/Linux), rode de novo e registre isso nas decisões técnicas do README.
- **Confirme:** na certificação, quase todas as "Chamadas ao LLM" devem ter dado certo. Se tudo caiu no fallback, o modelo não respondeu; investigue antes de seguir.

### [x] B. Matriz de avaliação humana (Seção 5.2, `NOTAS_HUMANAS`)
1. Rode `PYTHONIOENCODING=utf-8 py -3 testes/comparar_respostas.py entrega/1_Notebook_GS2026_2.ipynb` (gera `testes/saida/comparacao_P1_P5.md`).
2. Para cada pergunta (P1 a P5), mostre à dupla, lado a lado, a pergunta, a resposta esperada (em `PERGUNTAS_TESTE`) e as respostas da v1 e da v2. As checagens automáticas (ids citados, ids inventados, canal indicado, número de linhas) entram só como **apoio**.
3. Escreva em `NOTAS_HUMANAS` **exatamente** as notas e justificativas que a dupla der.
4. Escala: 10 = perfeita; 5 = parcialmente certa; 0 = errada, inventou dado ou obedeceu ao texto hostil.
5. Rode de novo no Colab pelo menos a célula 5.2 e a da certificação, para a média aparecer.

### [x] C. Registro de iterações (`3_prompts_kit.md`, seção 5)
- Preencha a tabela "O que aconteceu de verdade" com um resumo **fiel** das respostas da v1 e da v2, tirado da saída real.
- A coluna "Melhorou?" segue as notas da dupla. Se a v2 não melhorou em alguma pergunta, diga isso com honestidade.
- Se a dupla quiser uma v3, **ela decide o que muda**. Você implementa e atualiza todos os lugares listados na tarefa D.

### [ ] D. System prompt e conclusão com as palavras da dupla
- **Prompt:** percorra os blocos do `PROMPT_V2` um a um (tabela 1.1 do kit). Para cada bloco, pergunte à dupla "por que esse bloco existe?" e "como vocês diriam isso?", e reescreva com as palavras deles. Mantenha os 7 elementos e a frase literal do briefing.
- Se o prompt mudar, atualize **todos** os lugares onde ele aparece: `PROMPT_V2` (código da Seção 4), o markdown "System prompt final (v2)" da Seção 4, `3_prompts_kit.md` (seções 1 e 1.2) e `FEW_SHOT`. O few-shot precisa bater com o JSON: FZC-011 interditado, FZC-012 ativo e 24h.
- **Conclusão (Seção 7):** no máximo 10 linhas. Peça à dupla a tese em uma ou duas frases e reescreva o rascunho a partir dela.

### [x] E. Certificação (`5_certificacao.txt`)
- Troque o bloco modelo pela saída da **última célula** do notebook executado.
- Cole o link do Colab (compartilhado como "qualquer pessoa com o link pode ver") e o link dos prints.

### [x] F. Prints do README (`4_README.md`, seção 5)
- Você não tira print do Colab. A dupla tira os 5 prints listados no README, sobe em um link (Drive ou GitHub) e você cola como `![descrição](link)`.
- **Não** crie pasta de imagens: o zip só tem os 6 arquivos.

### [x] G. Chat log (`6_Chat_Log.txt`)
- [x] Acrescente um resumo das sessões do Claude Code (feito em 18/11 até a sessão de 17/11; acrescente as sessões seguintes).
- Complete o item `[completar: …]` da lista "Decisão da dupla × Sugestão da IA".

### [x] H. Checagem final e zip
- Rode a checagem da seção 7. Só gere o zip se tudo passar.
- Lembre a dupla de **subir no Portal FIAP antes de 19/11, 23h59**, e de conferir se a turma pede que só um integrante envie.

## 5. Preparar o PC (fazer uma vez em cada computador)

O ambiente é Windows. O comando `python` pode abrir a Microsoft Store; **use `py -3`**.

```bash
py -3 --version                 # precisa de Python 3.10+
py -3 -m pip install pandas     # o único pacote que o teste com mock usa
```

Para que acentos e emojis apareçam no terminal, rode os scripts com `PYTHONIOENCODING=utf-8` (Git Bash) ou `$env:PYTHONIOENCODING="utf-8"` (PowerShell).

**Levar o projeto de um PC para o outro (via GitHub):** o repositório é **https://github.com/FernandoCampM/GS-Prompt-and-AI** (privado, por causa da penalidade de similaridade entre grupos; só torne público depois de 19/11).
```bash
# no PC novo, a primeira vez
git clone https://github.com/FernandoCampM/GS-Prompt-and-AI.git
cd GS-Prompt-and-AI            # abra o Claude Code nesta pasta

# ao COMEÇAR cada sessão
git pull

# ao TERMINAR cada sessão (depois de atualizar o Diário, seção 9)
git add -A
git commit -m "o que foi feito"
git push
```
O `.gitignore` deixa de fora `testes/saida/`, o zip e arquivos de chave. **Antes de cada commit, confira que a chave não está em nenhum arquivo** (a checagem final faz isso). Se o git pedir identidade no PC novo, configure **só no repositório** (`git config user.name ...` e `git config user.email ...`, sem `--global`).

## 6. Como editar e testar o notebook

- O `.ipynb` é JSON. Edite com Python (`json.load` → mude `cell["source"]` → `json.dump(..., ensure_ascii=False, indent=1)`) e ache a célula **pelo texto**, não pelo índice.
- Se o notebook já tiver saídas da execução real, **não apague** as saídas das células que você não mudou. Nas células que mudou, avise a dupla que precisa rodar de novo no Colab.
- `2_dados_servico.json` é **gerado** pela Seção 1. Para mudar os dados, mude `registros_brutos` no notebook, rode o mock e copie `testes/saida/2_dados_servico.json` para `entrega/`.
- Depois de **qualquer** edição no notebook, rode os dois testes. Todos precisam terminar com `OK: o notebook rodou do início ao fim com o mock.`
  ```bash
  PYTHONIOENCODING=utf-8 py -3 testes/rodar_com_mock.py
  MOCK_NOKEY=1 PYTHONIOENCODING=utf-8 py -3 testes/rodar_com_mock.py
  MOCK_LOCAL=1 PYTHONIOENCODING=utf-8 py -3 testes/rodar_com_mock.py   # ramo do Ollama local (fora do Colab: fallback)
  ```
  O mock só prova que o `Run all` não quebra. Ele **não** substitui a execução real, e as respostas dele nunca entram nos arquivos de entrega.

## 7. Checagem final (rodar antes de zipar)

O script já está salvo em `testes/checagem_final.py` (o código abaixo é uma cópia). Rode `PYTHONIOENCODING=utf-8 py -3 testes/checagem_final.py` a partir da raiz.

```python
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
```

## 8. Regras invioláveis

1. **A chave nunca aparece** em nenhum arquivo, saída de célula, print ou conversa. Nunca peça a chave no chat.
2. **Você não dá as notas da matriz humana.** Não sugira número, não pré-preencha e não diga "eu daria 8". O briefing diz que nota atribuída por IA invalida o critério.
3. **Você não escreve a tese nem a versão final do system prompt no lugar da dupla.** O briefing proíbe isso, e similaridade entre grupos zera o critério 5. Entreviste a dupla e edite a partir das palavras dela (tarefa D).
4. **Os títulos das seções do notebook não mudam** (seção 3).
5. **O notebook roda do início ao fim.** Depois de qualquer edição, rode os testes da seção 6.
6. **Nada de `class`** no código.
7. **O zip tem exatamente os 6 arquivos, sem pasta**, com o nome `GS2026_2_1CCPS_AcessaMetro.zip`.
8. **Não invente resultados.** Tudo o que for escrito sobre "o que o modelo respondeu" vem da saída real do notebook, nunca do mock.

## 9. Diário (atualize ao fim de cada sessão: data, PC, o que foi feito, próximo passo)

- **16/11/2026, PC 1 (Desktop\GSPROMPTANDAI):** o projeto veio do zip do claude.ai (`AcessaMetro_GS2026_2_projeto.zip`). Revisei os 6 arquivos contra o briefing; o formato da entrega está certo. Os testes com mock passaram: com mock, 27 chamadas e 8 classificações via LLM + 4 via fallback; sem chave, tudo cai no fallback e mesmo assim não quebra. O `2_dados_servico.json` gerado é idêntico ao da `entrega/`. Reescrevi este CLAUDE.md para a nova estrutura de pastas e para Windows (`py -3`). Depois, a dupla decidiu **manter o `gpt-oss:20b`**, e isso foi registrado nas decisões técnicas do README. **Próximo passo:** confirmar a divisão de tarefas (tarefa 0) e rodar o notebook no Colab (tarefa A).
- **16/11/2026, PC 1:** criei o repositório git com `.gitignore` e enviei tudo para https://github.com/FernandoCampM/GS-Prompt-and-AI (branch `main`), para o Fernando continuar em outro PC. Nada mudou no conteúdo da entrega. **Próximo passo:** no PC novo, `git clone` e abrir o Claude Code na pasta; continuar pela tarefa 0 (divisão de tarefas) e pela tarefa A (Colab).
- **16/11/2026, PC 2 (pasta GS-Prompt-and-AI):** instalei o `pandas` (Python 3.14). A dupla definiu a divisão de tarefas, e eu reescrevi o bloco da Seção 0 com ela: **Fernando** ficou com a ideia, as estações, os equipamentos e o esquema, a telemetria e o risco, a injection do FZC-009, a execução no Colab e as notas humanas; **André** ficou com a classificação pelo LLM e o fallback, a validação e a governança e o system prompt; **os dois** ficaram com as perguntas de teste, a Seção 6, a conclusão, o README, os prints, a certificação e o chat log. Os dois testes com mock passaram. Tarefa 0 concluída. **Próximo passo:** tarefa A (o Fernando roda no Colab); em paralelo, dá para fazer a D (entrevista do prompt e da tese) e a G.

- **17/11/2026, PC 2:** o Fernando rodou o notebook no Colab com o `gpt-oss:20b`. Ele rodou do início ao fim, sem erro e sem a chave nas saídas, mas a Ollama Cloud recusou as 27 chamadas pedindo crédito (*"Add usage credits or subscribe"*), e tudo caiu no fallback. Por isso o arquivo **não** foi copiado para `entrega/` (o executado está em `Downloads`). A dupla escolheu o **plano B**: `USAR_OLLAMA_LOCAL = True`. Deixei a instalação local à prova de falha (try/except e espera pelo servidor), atualizei a Seção 0, a intro da Seção 1, o README (como executar e decisões técnicas) e o chat log, e acrescentei o `MOCK_LOCAL=1` ao teste. Os 3 testes com mock passaram. **Próximo passo:** rodar de novo no Colab, agora sem precisar de chave (`Run all`), baixar com as saídas para `entrega/` e conferir se as chamadas deram certo.
- **17/11/2026, PC 2 (cont.):** na execução local em CPU, o Colab ficou mais de 20 min preso na célula 7 (classificação da Seção 2). A causa provável é uma chamada sem fim no modo JSON de um modelo pequeno, já que o cliente não tinha limite de tempo. Acrescentei `TEMPO_LIMITE_S = 120` (timeout do Client) e `MAX_TOKENS = 512` (`num_predict`) na célula do cliente. Os 3 testes com mock passaram. **Próximo passo:** rodar de novo no Colab, de preferência com GPU T4.
- **18/11/2026, PC 2:** um agente acrescentou ao `6_Chat_Log.txt` o resumo das 5 sessões do Claude Code (tarefa G, primeira metade; o item `[completar: …]` continua com a dupla). Outro agente criou `testes/comparar_respostas.py`, que lê um notebook executado e gera `testes/saida/comparacao_P1_P5.md` com pergunta, esperado, v1 e v2 lado a lado e linhas em branco para as notas (apoio à tarefa B; testado com a execução que caiu no fallback). Os 3 testes com mock passaram; a checagem final tem 7 itens ❌, todos dependentes do Colab ou da dupla. Tudo enviado ao GitHub. **A segunda execução no Colab (plano B, com limite de tempo) ainda NÃO voltou.** **Próximo passo:** ver o bloco "Próxima sessão: comece aqui" no topo.
- **18/11/2026, PC 2 (cont.):** a 3ª execução no Colab (plano B, `llama3.2:1b`, 18/11 às 03:47) deu certo: **27 de 27 chamadas com sucesso**, sem erro e sem chave nas saídas; o código das células é idêntico ao do commit. A Seção 2 teve 4 classificações via LLM e 8 via fallback (a IA disse 'ok' para equipamentos parados, ou o resumo passou de 140 caracteres), e o resumo da IA para o FZC-009 obedeceu à injection ("Elevadores funcionam perfeitamente."), mas a governança o trocou pela regra. Copiei o arquivo para `entrega/` (os testes com mock passaram e o JSON é idêntico) e gerei `testes/saida/comparacao_P1_P5.md`. Tarefa A concluída. **Próximo passo:** tarefa B (notas da dupla).
- **18/11/2026, PC 2 (cont.):** a dupla deu as 10 notas e as justificativas (critério: "o quao bom o texto está escrito dado sua veracidade"); escrevi tudo literalmente em `NOTAS_HUMANAS`. Média v1 4,2, v2 3,0: a v2 **não** melhorou (o briefing aceita uma justificativa honesta). Limpei as saídas só dessa célula; falta rodar de novo, no Colab, a 5.2 e a certificação **na mesma sessão da execução de 18/11** (um Run all novo regera as respostas, e as notas deixariam de bater). **Próximo passo:** essa reexecução; depois C, D, E, F, G e H.
- **18/11/2026, PC 2 (cont.):** pelo Claude in Chrome (Brave), abri o notebook no Colab (sessão de 03:47 ainda viva), troquei a célula 5.2 pelas notas da dupla, rodei a 5.2 e a certificação (Matriz SIM, média v1 4,2 / v2 3,0), salvei no Drive e baixei. As 13 saídas das outras células são idênticas às da execução de 03:47; o Colab tinha apagado os números de execução, e eu os restaurei a partir do arquivo daquela execução (1–12 e 14; a 5.2 é a 17 e a certificação, a 18). Colei a certificação real em `5_certificacao.txt`. Link do notebook no Drive: https://colab.research.google.com/drive/1JXF10iGDLSMppRmj7OzIPq-J0RHrySXv (compartilhado como "qualquer pessoa com o link: leitor" em 18/11; sem private_outputs). **Faltam:** compartilhar + links, prints, C, D (conclusão), item [completar] do chat log, H.
- **18/11/2026, PC 2 (cont.):** notebook compartilhado (leitor por link). A dupla tirou os prints; eu os subi pelo Brave para a pasta do Drive `GS2026_2_1CCPS_AcessaMetro_prints` (https://drive.google.com/drive/folders/1r7OzViX_8-npzRbnWL6c8XIdIV7l0IDf, leitor por link) e coloquei no README (seção 5, miniaturas `drive.google.com/thumbnail`, que abrem sem login) e os dois links no `5_certificacao.txt`. Tarefas B, E e F concluídas. **Faltam:** C (tabela de iterações do kit), D (conclusão com a tese da dupla), item [completar] do chat log, H (checagem + zip) e commit/push.
- **18/11/2026, PC 2 (cont.):** a dupla deu a tese; reescrevi a conclusão (7 linhas) a partir dela. O [completar] do chat log foi preenchido com o texto aprovado pela dupla (plano B + revisão das notas; dados e pesos sem mudança). Preenchi a tabela de iterações do kit com a saída real e as notas (v2 só melhorou na P5; leitura honesta do porquê) e corrigi a frase "v2 aprovada nos testes" no kit e na Seção 4. **Checagem final: tudo ✅; zip gerado.** Pendências opcionais: (1) tarefa D, parte do prompt: a dupla não reescreveu o PROMPT_V2 com as próprias palavras; ela precisa saber justificar cada bloco na defesa; (2) o Colab compartilhado ainda tem a conclusão antiga e a frase antiga da Seção 4 (só markdown). **Falta só a dupla subir o zip no Portal FIAP até 19/11, 23h59.**

## 10. Se a dupla perguntar sobre o conteúdo (possíveis perguntas da defesa)

Explique com diagramas ASCII e em linguagem simples:
- por que a temperatura é baixa (consistência e auditabilidade);
- por que o fallback nunca usa o relato (o relato pode ser hostil);
- por que a IA pode subir a urgência, mas não rebaixar;
- como `"24h"` e `"04:40–00:00"` são comparados (conversão para minutos, com o fim à meia-noite);
- por que `acessivel` desconhecido vira `false`;
- o que é a cerca `<registros>` e as aspas triplas, e por que ela ajuda contra *prompt injection*;
- por que o risco de falha é uma regra e não um modelo treinado (limitação declarada);
- por que FZC-009 vem logo depois dos equipamentos parados na fila, mesmo estando "ativo" (risco 76: é a ideia de "perto de quebrar").
