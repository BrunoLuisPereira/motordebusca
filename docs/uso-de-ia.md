# Uso de IA no Desenvolvimento

## Ferramenta utilizada
Claude (Anthropic) — claude.ai

---

## Prompts Principais

### Prompt 1 — Planejamento geral
**Prompt:**
> "Tenho este enunciado de trabalho [colou o PDF]. Estou em trio, vou usar Python/FastAPI. Me dá um plano completo de desenvolvimento com estrutura de pastas, divisão de tarefas e arquitetura."

**O que a IA ajudou a produzir:**
- Estrutura de pastas completa do projeto
- Divisão de responsabilidades entre os membros do trio
- Diagrama do fluxo de dados entre os componentes
- Checklist de entregáveis mapeado para os critérios de avaliação

**O que foi ajustado manualmente:**
- Nomes dos membros do grupo
- Ajuste de portas no docker-compose para não conflitar com serviços já rodando na máquina

**Onde a IA foi genérica:**
- A divisão de tarefas foi sugerida de forma igual para todos os membros, sem considerar a diferença de experiência entre os integrantes

---

### Prompt 2 — Implementação dos algoritmos
**Prompt:**
> "Implemente os 4 algoritmos de substring search (Força Bruta, Rabin-Karp, KMP, Boyer-Moore) em Python seguindo o Strategy Pattern. Cada algoritmo deve ser uma classe independente com interface comum. Não pode usar indexOf() nem contains() na implementação."

**O que a IA ajudou a produzir:**
- Interface `SearchStrategy` com método `search()` e template method para medição de tempo
- Dataclass `SearchResult` com todos os campos exigidos pelo enunciado
- Implementação dos 4 algoritmos com comentários explicando cada etapa
- Registry central (`ALGORITHM_REGISTRY`) para troca em runtime
- Suite de testes com pytest cobrindo casos: padrão não encontrado, padrão igual ao texto, caracteres unicode, texto vazio, padrões sobrepostos

**O que foi corrigido manualmente:**
- O KMP inicial tinha um bug no caso em que `j != 0` e `text[i] != pattern[j]`: o índice `i` não era incrementado quando deveria, causando loop infinito em alguns inputs. Corrigido adicionando `elif i < n and text[i] != pattern[j]`.
- O Boyer-Moore no caso de match completo (quando `j < 0`) usava uma expressão de deslizamento que podia levantar `IndexError` no final do texto. Adicionado guard `if s + m < n`.

**Onde a IA errou:**
- A primeira versão do Rabin-Karp não tratava hashes negativos após o deslizamento da janela, causando falsos negativos. A IA mencionou o problema em comentário mas não adicionou o `if hash_window < 0: hash_window += mod`.

---

### Prompt 3 — Observabilidade com OpenTelemetry
**Prompt:**
> "Configure OpenTelemetry em FastAPI com Python. Preciso de: traces com 3 spans (file_load, algorithm_execution, format_result), métricas search_duration_ms (histogram), search_requests_total (counter) e document_size_chars (histogram) com labels algorithm e found, e logs estruturados de início e fim de busca. Exporte tudo via OTLP gRPC para um collector."

**O que a IA ajudou a produzir:**
- Arquivo `otel_setup.py` completo com TracerProvider, MeterProvider e LoggerProvider
- Configuração do `BatchSpanProcessor` e `PeriodicExportingMetricReader`
- Integração dos instrumentos no endpoint `/search` com atributos nos spans
- `docker-compose.yml` com OTEL Collector + Prometheus + Tempo + Grafana
- Arquivos de configuração de cada serviço
- Dashboard JSON do Grafana com painéis para todas as métricas exigidas

**O que foi ajustado manualmente:**
- O namespace das métricas no collector precisou ser ajustado de `search` para `motor_busca` para corresponder ao que o Grafana esperava nas queries PromQL do dashboard
- A porta do Tempo no docker-compose conflitava com a porta 4317 do collector: remapeada para 4319 externamente

**Onde a IA foi genérica demais:**
- O dashboard JSON gerado usava nomes de métricas genéricos que não correspondiam exatamente ao formato gerado pelo exporter OTLP → Prometheus (que adiciona sufixos como `_total`, `_sum`, `_count`, `_bucket`). Foi necessário testar e ajustar as queries PromQL manualmente após subir a stack.
- A IA não previu a necessidade do `allowUiUpdates: true` no provisionamento do Grafana, o que impedia editar o dashboard pela interface.

---

## Resumo

| Aspecto | Avaliação |
|---------|-----------|
| Estrutura e arquitetura | ✅ Excelente ponto de partida |
| Algoritmos (lógica central) | ✅ Corretos, com bugs pontuais identificáveis |
| OpenTelemetry setup | ✅ Funcional, requer ajuste fino de nomes |
| Docker/infra | ✅ Funcional, requer ajuste de portas |
| Testes | ✅ Cobertura abrangente gerada automaticamente |
| Dashboard PromQL | ⚠️ Queries precisaram de correção manual |

A IA acelerou significativamente o desenvolvimento, especialmente na parte de infraestrutura (OpenTelemetry + Docker) que seria a mais demorada para pesquisar do zero. O código dos algoritmos foi revisado linha a linha para garantir compreensão e corretude antes da entrega.
