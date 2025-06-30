import numpy as np
import threading
from typing import Dict, List


# Parte 3: Paralelismo e Concorrência Avançada


# Lista 03 - simulations.py
def sma(returns: np.ndarray, window: int) -> np.ndarray:
    """
    Calcula a Média Móvel Simples (SMA) para um vetor de retornos.

    Args:
        returns (np.ndarray): Vetor de retornos.
        window (int): Tamanho da janela para a média móvel.

    Returns:
        np.ndarray: Vetor de médias móveis.
    """
    if window <= 0:
        raise ValueError("O tamanho da janela deve ser maior que zero.")
    if len(returns) < window:
        raise ValueError(
            "O vetor de retornos deve ter pelo menos 'window' elementos."
        )

    # Inicializando o vetor de somas móveis
    sum_values = np.zeros(len(returns) - window + 1)

    # Calculando a soma dos primeiros 'window' retornos
    sum_values[0] = np.sum(returns[: window])

    # Calculando as somas móveis subsequentes
    for i in range(1, len(sum_values)):
        delta_sum = returns[i + window - 1] - returns[i - 1]
        sum_values[i] = sum_values[i - 1] + delta_sum

    # Calculando a média móvel dividindo pela janela
    return sum_values / window


# 5. Processamento Paralelo de Dados de Múltiplas Ações
def calcular_medias_moveis(
    acoes: Dict[str, np.ndarray],
    janela: int,
) -> Dict[str, np.ndarray]:
    """
    Calcula as médias móveis simples (SMA) para múltiplas ações em paralelo.

    Args:
        acoes (Dict[str, np.ndarray]):
            Dicionário onde as chaves são os nomes das ações e os valores são
            arrays numpy com os preços das ações.
        janela (int): Tamanho da janela para a média móvel.

    Returns:
        Dict[str, np.ndarray]: Dicionário com as médias móveis simples para
        cada ação.
    """
    # Inicializando o dicionário para armazenar os resultados
    resultados = {}

    # Criando uma lista de threads para processar cada ação
    threads = []

    # Lock para garantir acesso seguro ao dicionário compartilhado
    lock = threading.Lock()

    # Função que será executada por cada thread para calcular a média móvel
    def processar_acao(nome: str, precos: np.ndarray):
        media = sma(precos, janela)
        # Garante acesso exclusivo ao dicionário compartilhado
        with lock:
            resultados[nome] = media

    for nome, precos in acoes.items():
        t = threading.Thread(target=processar_acao, args=(nome, precos))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return resultados


# 6. Simulação de Cálculo de Volatilidade Concorrente
def calcular_volatilidade(
    retornos: np.ndarray,
    janela: int,
    num_threads: int,
) -> np.ndarray:
    """
    Calcula a volatilidade (desvio padrão) de retornos em janelas móveis
    de forma concorrente, dividindo o trabalho entre várias threads.

    Args:
        retornos: Array NumPy de retornos diários.
        janela: Tamanho da janela para o cálculo da volatilidade.
        num_threads: Número de threads a serem usadas.

    Returns:
        Um array NumPy com as volatilidades calculadas para cada janela.
    """
    # Número total de cálculos de volatilidade a serem feitos.
    total_calculos = len(retornos) - janela + 1

    # Lista para manter as referências das threads.
    threads = []

    # Lista de listas para armazenar os resultados de cada thread
    # separadamente. Isso evita a necessidade de um Lock, pois não há
    # recurso compartilhado para escrita.
    resultados_por_thread = [[] for _ in range(num_threads)]

    # Determina o tamanho do "lote" de trabalho para cada thread.
    tamanho_lote = total_calculos // num_threads

    # Função que será executada por cada thread para calcular a volatilidade
    def vol(
        retornos: np.ndarray,
        janela: int,
        start_index: int,
        end_index: int,
        resultados: List[float]
    ):
        for i in range(start_index, end_index):
            janela_de_dados = retornos[i: i + janela]
            volatilidade = np.std(janela_de_dados)
            resultados.append(volatilidade)

    for i in range(num_threads):
        # Define o índice de início e fim dos cálculos para a thread atual.
        start_index = i * tamanho_lote
        end_index = (i + 1) * tamanho_lote

        # Garante que a última thread processe todos os cálculos restantes.
        if i == num_threads - 1:
            end_index = total_calculos

        # Cria a thread, passando a função worker e os argumentos necessários.
        thread = threading.Thread(
            target=vol,
            args=(
                retornos,
                janela,
                start_index,
                end_index,
                resultados_por_thread[i],
            )
        )
        threads.append(thread)
        thread.start()

    # Espera que todas as threads terminem seu trabalho.
    for thread in threads:
        thread.join()

    # Combina os resultados das listas individuais em uma única lista
    # final, na ordem correta.
    volatilidade_final = []
    for lista_resultado in resultados_por_thread:
        volatilidade_final.extend(lista_resultado)

    return np.array(volatilidade_final)
