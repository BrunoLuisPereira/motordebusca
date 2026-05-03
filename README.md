# Motor de Busca em Documentos

Aplicação web para pesquisa de palavras e trechos em documentos de texto, implementando algoritmos de substring search com observabilidade via OpenTelemetry.

**Disciplina:** Algoritmos Avançados  
**Integrantes:**
- Bruno Luis Pereira
- Rafael Pereira
- Ramires Silva Paes

---

## Algoritmos Implementados

| Algoritmo | Complexidade | Estratégia |
|-----------|-------------|-----------|
| Força Bruta (Naive) | O(N·M) pior caso | Comparação direta char a char |
| Rabin-Karp | O(N+M) esperado | Hash rolante |
| KMP | O(N+M) garantido | Tabela LPS (falhas) |
| Boyer-Moore | O(N/M) melhor caso | Heurística Bad Character |

---

## Estrutura do Projeto

```
motor-de-busca/
├── backend/
│   ├── main.py
│   ├── telemetry.py
│   ├── algorithms/
│   │   ├── strategy.py
│   │   ├── brute_force.py
│   │   ├── rabin_karp.py
│   │   ├── kmp.py
│   │   └── boyer_moore.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   └── index.html               # Interface web (tela única)
├── observability/
│   ├── otel-collector-config.yml
│   ├── prometheus.yml
│   ├── tempo.yml
│   └── grafana/
│       ├── provisioning/        # Datasources + dashboards auto-provisionados
│       └── dashboards/
│           └── motor-busca.json
├── tests/
│   └── test_algorithms.py
├── docs/
│   └── uso-de-ia.md
└── docker-compose.yml
```

---

## Pré-requisitos

- Python 3.12+
- Docker + Docker Compose

---

## Instalação e Execução

### 1. Clonar o repositório

```bash
git clone <url-do-repo>
cd motor-de-busca
```

### 2. Subir toda a stack (app + observabilidade)

```bash
docker-compose up --build
```

Aguarde todos os serviços iniciarem.

| Serviço | URL |
|---------|-----|
| Backend API | http://localhost:8000 |
| Frontend | abrir `frontend/index.html` no navegador |
| Grafana | http://localhost:3000 (admin / admin) |
| Prometheus | http://localhost:9090 |
| API Docs (Swagger) | http://localhost:8000/docs |

### 3. (Alternativa) Rodar o backend localmente sem Docker

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

> **Nota:** sem Docker o OTEL Collector não estará disponível. A busca funciona normalmente, mas a observabilidade completa depende da stack Docker.

---

## Executar os Testes

```bash
# Na raiz do projeto
pip install pytest
pytest tests/test_algorithms.py -v
```

---

## Como Usar a Aplicação

1. Abra `frontend/index.html` no navegador.
2. Faça upload de um arquivo `.txt`.
3. Selecione o algoritmo no dropdown.
4. Digite o termo ou trecho a pesquisar.
5. Clique em **Pesquisar**.
6. Veja os resultados: encontrado?, tempo (ms), ocorrências, posições, N e M.

---

## Documentos de Teste

| Documento | Uso |
|-----------|-----|
| Bíblia (~4 MB) | Stress test com N grande |
| Os Lusíadas | Caracteres especiais / acentuação |
| A Catedral e o Bazar | Texto técnico em inglês |
| _(obra escolhida)_ | Qualquer domínio público |

---

## Dashboard de Observabilidade

Acesse **http://localhost:3000** → Dashboards → **Motor de Busca — Observabilidade**.

O dashboard exibe:
- Total de buscas e buscas com resultado encontrado
- Tempo médio de busca por algoritmo (série temporal)
- Histograma de distribuição de tempo
- Comparativo em tabela entre algoritmos
- Tamanho médio dos documentos processados

---

## Arquitetura de Observabilidade

```
FastAPI (app)
    │  OTLP gRPC :4317
    ▼
OTEL Collector
    ├──► Prometheus :8889  →  Grafana (métricas)
    └──► Tempo :4317       →  Grafana (traces)
```

**Traces:** um trace por requisição, com spans para `file_load`, `algorithm_execution` e `format_result`.  
**Métricas:** `search_duration_ms` (histogram), `search_requests_total` (counter), `document_size_chars` (histogram).  
**Logs:** início e fim de cada busca com algoritmo, N, M, tempo e ocorrências.