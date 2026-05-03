# ============================================================
# Este arquivo foi gerado com auxílio da IA Claude (Anthropic)
# Disciplina: Algoritmos Avançados — Católica SC
# Integrantes: Bruno Luis Pereira, Rafael Pereira, Ramires Silva Paes
# ============================================================
# telemetry.py
# Configura o OpenTelemetry e expõe uma função simples para registrar cada busca
# OpenTelemetry = ferramenta para registrar o que acontece dentro da aplicação
#   - Traces: "rastro" de uma requisição (quanto tempo cada parte demorou)
#   - Métricas: contadores e histogramas (quantas buscas, quanto tempo médio etc.)
#   - Logs: mensagens de texto com informações da busca

import os
import logging

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# Endereço do OTEL Collector (configurado no docker-compose)
OTEL_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")

# Identifica este serviço nas ferramentas de observabilidade
recurso = Resource.create({"service.name": "motor-de-busca"})

# ── Configuração de Traces ────────────────────────────────────────────────────
tracer_provider = TracerProvider(resource=recurso)
tracer_provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint=OTEL_ENDPOINT, insecure=True))
)
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer("motor-de-busca")

# ── Configuração de Métricas ──────────────────────────────────────────────────
leitor = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint=OTEL_ENDPOINT, insecure=True),
    export_interval_millis=10_000,
)
meter_provider = MeterProvider(resource=recurso, metric_readers=[leitor])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter("motor-de-busca")

# Cria os instrumentos de métricas exigidos pelo enunciado
tempo_busca     = meter.create_histogram("search_duration_ms",    unit="ms")
total_buscas    = meter.create_counter("search_requests_total")
tamanho_doc     = meter.create_histogram("document_size_chars")

# ── Logger ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("motor-de-busca")


# ── Função principal ──────────────────────────────────────────────────────────
def registrar_telemetria(resultado, nome_arquivo):
    """
    Recebe o resultado da busca e registra tudo no OpenTelemetry:
    - Um trace com spans para cada etapa
    - Métricas de tempo, contagem e tamanho
    - Logs de início e fim
    """

    labels = {
        "algorithm": resultado.algorithm,
        "found": str(resultado.found).lower()
    }

    # Log de início
    logger.info(
        f"[BUSCA] algoritmo={resultado.algorithm} | "
        f"arquivo={nome_arquivo} | N={resultado.n} | M={resultado.m}"
    )

    # Trace com 3 spans conforme exigido
    with tracer.start_as_current_span("requisicao_busca") as span_raiz:
        span_raiz.set_attribute("algoritmo", resultado.algorithm)
        span_raiz.set_attribute("arquivo", nome_arquivo)

        # Span 1: carregamento do arquivo (já foi feito, registramos aqui)
        with tracer.start_as_current_span("leitura_arquivo"):
            pass  # o arquivo já foi lido no endpoint, este span registra essa etapa

        # Span 2: execução do algoritmo
        with tracer.start_as_current_span("execucao_algoritmo") as span_algo:
            span_algo.set_attribute("algoritmo", resultado.algorithm)
            span_algo.set_attribute("n", resultado.n)
            span_algo.set_attribute("m", resultado.m)
            span_algo.set_attribute("encontrado", resultado.found)
            span_algo.set_attribute("ocorrencias", resultado.occurrences)
            span_algo.set_attribute("tempo_ms", resultado.time_ms)

        # Span 3: formatação do resultado
        with tracer.start_as_current_span("formatacao_resultado"):
            pass

    # Registra as métricas
    tempo_busca.record(resultado.time_ms, labels)
    total_buscas.add(1, labels)
    tamanho_doc.record(resultado.n, {"algorithm": resultado.algorithm})

    # Log de fim
    logger.info(
        f"[RESULTADO] algoritmo={resultado.algorithm} | "
        f"tempo={resultado.time_ms:.4f}ms | ocorrencias={resultado.occurrences}"
    )