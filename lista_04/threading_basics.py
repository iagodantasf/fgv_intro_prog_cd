import threading
import random
import time
from typing import Dict, List, Any


# Parte 1: Introdução ao Multithreading


# 1. Simulação de Traders Colocando Ordens Concorrentemente
def simular_traders(
    num_traders: int,
    num_ordens: int,
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Simula a colocação de ordens por múltiplos traders de forma concorrente.

    Args:
        num_traders (int): Número de traders.
        num_ordens (int): Número de ordens por trader.

    Returns:
        Dict[str, List[Dict[str, Any]]]:
            Dicionário com chaves 'buy' e 'sell', contendo listas de ordens.
            Cada ordem é um dicionário com 'id', 'price' e 'quantity'.
    """
    ordens = {"buy": [], "sell": []}

    # Setando a seed para reprodutibilidade
    random.seed(42)

    # Lock para garantir acesso seguro às ordens compartilhadas
    lock = threading.Lock()

    # Função que simula o comportamento de um trader
    def trader(trader_id: int):
        for i in range(num_ordens):
            # Definindo lado da ordem (1 para compra, 0 para venda)
            side = random.randint(0, 1)

            if side == 1:  # Compra num valor mais baixo
                key = "buy"
                price = round(random.uniform(80, 99.9), 2)
            else:  # Venda num valor mais alto
                key = "sell"
                price = round(random.uniform(100.1, 120), 2)

            # Construindo a ordem
            ordem = {
                "id": f"trader_{trader_id}_ordem_{i+1}",
                "price": price,
                "quantity": random.randint(1, 10) * 100,  # Múltiplos de 100
            }

            # Adicionando a ordem ao dicionário de ordens
            with lock:
                ordens[key].append(ordem)

    threads = []
    for i in range(num_traders):
        thread = threading.Thread(target=trader, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return ordens


# 2. Simulação de Feeds de Dados Concorrentes
def simular_feeds_de_dados(
    acoes: List[str],
    tempo_total: int,
) -> Dict[str, float]:
    """
    Simula feeds de dados concorrentes para atualizar preços de ações.

    Args:
        acoes (List[str]): Lista de nomes de ações.
        tempo_total (int): Tempo total de simulação em segundos.

    Returns:
        Dict[str, float]: Dicionário final de preços após a simulação.
    """
    # Setando a seed para reprodutibilidade
    random.seed(42)

    # Inicializando o dicionário de preços com valores aleatórios
    prices = {
        acao: round(random.uniform(5, 25), 2)
        for acao in acoes
    }

    # Lock para garantir acesso seguro ao dicionário de preços compartilhado
    lock = threading.Lock()

    # Evento para parar as threads
    parar_evento = threading.Event()

    # Função para atualizar preços
    def atualizar_preco(acao: str):
        while not parar_evento.is_set():
            with lock:
                prices[acao] += random.gauss(0, 1)
                prices[acao] = round(prices[acao], 2)
                if prices[acao] < 0:  # Evitando preços negativos
                    prices[acao] = 1
            time.sleep(random.randint(1, 3))

    # Função para imprimir os preços atuais a cada 5 segundos
    def imprimir_precos():
        while not parar_evento.is_set():
            with lock:
                print(prices)
            time.sleep(5)

    # Criando e iniciando as threads para cada ação
    threads = []
    for acao in acoes:
        thread = threading.Thread(target=atualizar_preco, args=(acao,))
        threads.append(thread)
        thread.start()

    # Criando e iniciando a thread para imprimir os preços
    imprimir_thread = threading.Thread(target=imprimir_precos)
    imprimir_thread.start()

    # Aguardando o tempo total de simulação
    time.sleep(tempo_total)
    parar_evento.set()  # Sinaliza para todas as threads que é hora de parar

    # Parando todas as threads de atualização de preços
    for thread in threads:
        thread.join()

    # Parando a thread de impressão
    imprimir_thread.join()

    return prices
