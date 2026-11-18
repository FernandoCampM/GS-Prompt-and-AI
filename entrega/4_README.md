# Acessa Metrô — GS2026.2 CitizenTech

**Prompt and Artificial Intelligence** · Prof. Jorge Luiz Gomes · Ciência da Computação, 1º semestre
**Turma:** 1CCPS · **Modalidade:** dupla · **Frente:** C — Acessibilidade

| Integrante | RM |
|---|---|
| Fernando Campos Garnica Mota | 567451 |
| André da Silva Pinto | 559038 |

---

## 1. O problema

Elevadores, escadas rolantes e esteiras rolantes das estações de metrô ficam horas, dias ou até semanas parados. Quando são consertados, muitas vezes voltam a quebrar pouco tempo depois. Quem mais sofre é quem depende deles: cadeirantes, idosos, pessoas com mobilidade reduzida e quem carrega peso.

Hoje existem dois buracos de informação:
- **O cidadão** não sabe, antes de chegar, se o equipamento funciona nem qual é a alternativa que serve para ele.
- **O técnico** sabe o que já quebrou, mas não sabe o que está **perto** de quebrar. Por isso a manutenção corre atrás do problema em vez de evitá-lo.

## 2. A solução

O Acessa Metrô usa uma base de equipamentos com telemetria (simulada no estilo de um monitoramento Zabbix: disponibilidade, falhas, horas parado, última manutenção) e entrega duas coisas:

```
                    2_dados_servico.json  (12 equipamentos, 7 estações)
                                 │
           ┌─────────────────────┴─────────────────────┐
           ▼                                           ▼
   risco_falha (regra 0–100)                 assistente "Acessa Metrô"
   + urgência pelo LLM                       (system prompt v2, llama3.2:1b via Ollama no Colab)
   + validação e fallback                              │
           │                                           ▼
           ▼                              CIDADÃO: "o elevador da Sé funciona?"
   TÉCNICO: fila de prioridade             → status + alternativa acessível
   (parados primeiro, depois os              + "Fonte: baseado no registro FZC-00X"
    mais perto de quebrar)
```

**ODS:** 11 (meta 11.2, transporte acessível para pessoas com deficiência e idosos) e 10 (meta 10.2, inclusão).

## 3. Como executar

1. Abra `1_Notebook_GS2026_2.ipynb` no Google Colab.
2. `Runtime → Run all`. Não precisa de chave: com `USAR_OLLAMA_LOCAL = True` (o padrão da entrega), a célula do cliente instala o Ollama no próprio Colab e baixa o `llama3.2:1b` (de 1 a 3 minutos na primeira vez).
3. *(Opcional, para usar a nuvem)* mude `USAR_OLLAMA_LOCAL = False`, clique no ícone de chave (🔑 **Secrets**), crie o segredo `OLLAMA_API_KEY` e ative "Notebook access".
4. Ao final, a última célula imprime a **certificação** (copiada para `5_certificacao.txt`).

- **O modelo não respondeu?** O notebook não quebra: se a instalação local falhar (ou, na nuvem, faltar chave ou crédito), todas as etapas com IA caem no fallback por regra, e isso aparece na coluna `fonte` e na certificação.
- **O Colab caiu no meio?** Rode de novo a partir da Seção 1. O `2_dados_servico.json` é regravado e não depende do LLM.
- A chave **nunca** aparece no código: é lida com `userdata.get('OLLAMA_API_KEY')`.

## 4. Arquivos da entrega

| Arquivo | Conteúdo |
|---|---|
| `1_Notebook_GS2026_2.ipynb` | Notebook completo, Seções 0 a 7 |
| `2_dados_servico.json` | 12 registros validados (gerado pelo notebook) |
| `3_prompts_kit.md` | System prompt final, v1, classificador, few-shot, justificativas e iterações |
| `4_README.md` | Este arquivo |
| `5_certificacao.txt` | Saída final do notebook + links + nomes e RMs |
| `6_Chat_Log.txt` | Registro do uso de IA como ferramenta |

## 5. Prints

*(Substituir pelos prints da execução de vocês)*

1. **Run all concluído:** Seção 1 com a tabela de correções e o JSON salvo.
2. **Seção 2:** tabela relato original × resumo da IA.
3. **Seção 3:** tabela de auditoria com a coluna `fonte` e a fila de prioridade da manutenção.
4. **Seção 5:** respostas v1 × v2 e a matriz de notas humanas.
5. **Certificação final.**

> Dica: o zip não deve ter pasta extra. Para colocar as imagens, suba os prints em um link (Drive ou GitHub) e cole aqui com `![descrição](link)`, ou cole os links no `5_certificacao.txt`.

## 6. Decisões técnicas

| Decisão | Por quê |
|---|---|
| **`acessivel` = "atende quem usa cadeira de rodas"** | Para a frente C, o booleano precisa responder a uma pergunta útil. Elevador e esteira plana = `true`; escada rolante = `false`. Assim o assistente nunca indica uma escada rolante como alternativa para cadeirante. |
| **Telemetria simulada (estilo Zabbix)** | Não dá para integrar um Zabbix real no Colab sem infraestrutura nem API paga. Os campos `disponibilidade_30d`, `falhas_30d`, `horas_parado` e `ultima_manutencao` imitam o que um monitoramento exportaria. |
| **Risco de falha por regra, não por IA** | `falhas_30d × 10 + (100 − disponibilidade) × 0,5 + 15 se a última manutenção foi há mais de 120 dias`, limitado a 100. É simples, mas qualquer técnico refaz a conta na mão, e é isso que deixa a prioridade auditável. |
| **Interpretação da regra 1** | O texto da regra 1 no briefing é ambíguo; seguimos a tabela do esquema: se o status **não** é `ativo`, o motivo é obrigatório. Motivo vazio vira "Motivo não informado pela operação" e é contado. |
| **`acessivel` desconhecido vira `false`** | Na dúvida, é melhor não prometer acessibilidade do que mandar um cadeirante para um equipamento que não serve. |
| **Horário normalizado para minutos** | `"08:00"` é texto. Convertemos para minutos antes de comparar, tratamos o fim à meia-noite (`04:40–00:00`) e o caso `"24h"`. |
| **Modelo `llama3.2:1b` rodando no próprio Colab (plano B)** | A escolha inicial da dupla era o `gpt-oss:20b` na Ollama Cloud. Na execução de 17/11, a nuvem recusou as 27 chamadas pedindo crédito (*"Add usage credits or subscribe"*), e o briefing exige rodar sem API paga. Por isso a dupla ativou o plano B (`USAR_OLLAMA_LOCAL = True`): o Ollama é instalado no Colab e roda o `llama3.2:1b`, grátis e sem chave. O modelo é bem menor, o que pesa na qualidade das respostas (ver a matriz da Seção 5). O código da nuvem continua no notebook. Nos dois casos, toda saída do modelo passa pela validação da Seção 3. |
| **Temperatura 0,1 (classificação) e 0,2 (assistente)** | Respostas estáveis: o mesmo registro deve receber sempre a mesma classe, e a mesma pergunta deve dar a mesma resposta (critério de consistência). |
| **Fallback nunca usa o relato** | O relato do cidadão pode ser hostil (o FZC-009 tem uma injection de propósito). Quando a resposta da IA é rejeitada, o resumo é montado só com o dado oficial. |
| **IA pode subir a urgência, mas não rebaixar** | Se a IA disser `ok` para um elevador interditado, a resposta é rejeitada e a regra assume. Se ela for mais cautelosa que a regra, aceitamos. |
| **Regra → IA → humano** | Todo caso `urgente` ou que caiu no fallback é marcado com `revisao_humana = True`. |
| **Trilha de auditoria** | Toda chamada ao modelo é registrada com a etapa, a versão do prompt, a temperatura e se deu certo (`trilha_auditoria.json`). |
| **Cerca nos dados** | Na v2, os registros vão dentro de `<registros>` e a pergunta entre aspas triplas, e o prompt declara que esses textos são dados, não instruções. |

## 7. Limitações

- Dados simulados, não em tempo real; nomes das estações são reais, mas status, números e relatos são fictícios.
- O risco de falha é uma heurística, não um modelo preditivo treinado com histórico real.
- Cobre 12 equipamentos em 7 estações (Linhas 1, 2 e 3). Não responde sobre outras estações, CPTM, ônibus ou outras cidades.
- Não informa previsão de conserto, horário de trem, tarifa ou rota, e não abre chamado de manutenção.
- O relato do cidadão não é verificado.
- O metrô é operado pelo estado; no cenário da GS, a Secretaria de Cidadania usa os dados em parceria com a operadora.

## 8. Como a IA foi usada

- **No desenvolvimento:** usamos o Claude para rascunhar o código, sugerir a estrutura do prompt e revisar textos. A ideia (monitorar a saúde dos equipamentos para manter o funcionamento perto de 100% e priorizar a manutenção), a escolha da frente, a fórmula de risco, as regras de fallback e as **notas da matriz de avaliação** são da dupla. Registro completo em `6_Chat_Log.txt`.
- **Dentro da solução:** o modelo `llama3.2:1b` (Ollama no Colab) classifica a urgência, reescreve o relato e responde como assistente. Toda saída dele é validada antes de ser usada.
