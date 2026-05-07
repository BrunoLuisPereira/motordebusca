# test_algorithms.py
# Testes simples para verificar se os algoritmos funcionam corretamente
# Executa com: pytest tests/test_algorithms.py -v

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.algorithms import ALGORITMOS

# Lista de todos os algoritmos para testar todos juntos
todos = list(ALGORITMOS.values())


def achar_posicoes_referencia(texto, padrao):
    """Usa o find() do Python apenas como referência para validar os resultados."""
    posicoes = []
    inicio = 0
    while True:
        idx = texto.find(padrao, inicio)
        if idx == -1:
            break
        posicoes.append(idx)
        inicio = idx + 1  # avança 1 posição para encontrar ocorrências sobrepostas
    return posicoes


# ── Testes ──────────────────────────────────────────────────────────────────

def test_achou_simples():
    for alg in todos:
        r = alg.search("abcabc", "abc")
        assert r.found is True
        assert r.occurrences == 2
        assert r.positions == [0, 3], f"Erro em {alg.name}"

def test_nao_achou():
    for alg in todos:
        r = alg.search("hello world", "xyz")
        assert r.found is False
        assert r.occurrences == 0
        assert r.positions == [], f"Erro em {alg.name}"

def test_uma_ocorrencia():
    for alg in todos:
        r = alg.search("the quick brown fox", "fox")
        assert r.positions == [16], f"Erro em {alg.name}"

def test_multiplas_ocorrencias():
    for alg in todos:
        texto = "the cat sat on the mat"
        padrao = "the"
        esperado = achar_posicoes_referencia(texto, padrao)
        r = alg.search(texto, padrao)
        assert r.positions == esperado, f"Erro em {alg.name}"

def test_padrao_igual_ao_texto():
    for alg in todos:
        r = alg.search("python", "python")
        assert r.positions == [0], f"Erro em {alg.name}"

def test_padrao_maior_que_texto():
    for alg in todos:
        r = alg.search("hi", "hello world")
        assert r.found is False, f"Erro em {alg.name}"

def test_texto_vazio():
    for alg in todos:
        r = alg.search("", "abc")
        assert r.found is False, f"Erro em {alg.name}"

def test_caractere_unico():
    for alg in todos:
        r = alg.search("banana", "a")
        assert r.occurrences == 3, f"Erro em {alg.name}"

def test_acentuacao():
    for alg in todos:
        r = alg.search("Os Lusíadas de Camões", "Lusíadas")
        assert r.found is True, f"Erro em {alg.name}"

def test_todos_retornam_mesmo_resultado():
    """Os 4 algoritmos devem retornar as mesmas posições para a mesma entrada."""
    texto = "abracadabra"
    padrao = "abr"
    resultados = [alg.search(texto, padrao).positions for alg in todos]
    for r in resultados[1:]:
        assert r == resultados[0], f"Algoritmos retornaram resultados diferentes!"

def test_metadados_do_resultado():
    alg = ALGORITMOS["kmp"]
    r = alg.search("hello world", "world")
    assert r.n == 11
    assert r.m == 5
    assert r.time_ms >= 0
    assert r.algorithm == "kmp"
