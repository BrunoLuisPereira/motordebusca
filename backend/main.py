# ============================================================
# Este arquivo foi gerado com auxílio da IA Claude (Anthropic)
# Disciplina: Algoritmos Avançados — Católica SC
# Integrantes: Bruno Luis Pereira, Rafael Pereira, Ramires Silva Paes
# ============================================================
# main.py
# Backend da aplicação — feito com FastAPI
# Tem dois endpoints:
#   GET  /algoritmos  → lista os algoritmos disponíveis
#   POST /buscar      → recebe o arquivo + algoritmo + padrão e retorna o resultado

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from algorithms import ALGORITMOS
from telemetry import registrar_telemetria

app = FastAPI(title="Motor de Busca")

# Permite o frontend (arquivo HTML local) chamar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/algoritmos")
def listar_algoritmos():
    """Retorna a lista de algoritmos disponíveis."""
    return {"algoritmos": list(ALGORITMOS.keys())}


@app.post("/buscar")
async def buscar(
    arquivo: UploadFile = File(...),
    algoritmo: str = Form(...),
    padrao: str = Form(...),
):
    # Valida se o algoritmo existe
    if algoritmo not in ALGORITMOS:
        raise HTTPException(status_code=400, detail=f"Algoritmo '{algoritmo}' não existe.")

    if not padrao:
        raise HTTPException(status_code=400, detail="O padrão não pode ser vazio.")

    # Lê o arquivo enviado
    conteudo = await arquivo.read()
    try:
        texto = conteudo.decode("utf-8")
    except UnicodeDecodeError:
        texto = conteudo.decode("latin-1")

    # Executa a busca com o algoritmo escolhido
    # Converte para minúsculas para busca case-insensitive
    # O texto original é mantido para exibir os trechos corretamente
    strategy = ALGORITMOS[algoritmo]
    resultado = strategy.search(texto.lower(), padrao.lower())

    # Registra telemetria (traces + métricas + logs)
    registrar_telemetria(resultado, arquivo.filename or "desconhecido")

    # Retorna o resultado como JSON
    return JSONResponse({
        "encontrado":   resultado.found,
        "ocorrencias":  resultado.occurrences,
        "posicoes":     resultado.positions[:500],
        "tempo_ms":     resultado.time_ms,
        "n":            resultado.n,
        "m":            resultado.m,
        "algoritmo":    resultado.algorithm,
        "texto":        texto,  # texto original para mostrar trechos no frontend
    })


@app.get("/health")
def health():
    return {"status": "ok"}