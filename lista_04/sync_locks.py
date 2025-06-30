import threading
import time
import random
from typing import List, Tuple, Dict


# Parte 2: Sincronização com Locks


# 3. Gerenciamento de Risco Concorrente
def gerenciar_risco(
    total_risco: float,
    estrategias: List[Tuple[str, float]],
    tempo_total: int,
) -> Dict[str, float]:
    risco_alocado = {nome: 0.0 for nome, _ in estrategias}
    risco_atual = [0.0]  # Lista para tornar mutável dentro da thread

    # Lock para garantir acesso seguro ao risco atual
    lock = threading.Lock()

    # Evento para parar as threads
    stop_event = threading.Event()

    # Função para simular a alocação de risco por estratégia
    def estrategia_thread(nome: str, risco_desejado: float):
        while not stop_event.is_set():
            with lock:
                if risco_atual[0] + risco_desejado <= total_risco:
                    risco_atual[0] += risco_desejado
                    risco_alocado[nome] += risco_desejado
            time.sleep(1)

    # Criar e iniciar threads
    threads = []
    for nome, risco in estrategias:
        t = threading.Thread(target=estrategia_thread, args=(nome, risco))
        t.start()
        threads.append(t)

    # Rodar simulação pelo tempo total
    time.sleep(tempo_total)
    stop_event.set()

    # Esperar todas as threads terminarem
    for t in threads:
        t.join()

    return risco_alocado


# 4. Monitoramento Concorrente de Ações
def monitorar_acoes(acoes: List[str], valor_alvo: float) -> List[str]:
    """
    Simula o monitoramento concorrente de ações utilizando múltiplas
    sthreads.

    Args:
        acoes (List[str]): Lista de nomes de ações a serem monitoradas.
        valor_alvo (float): Valor monitorado nas oscilações de preço.

    Returns:
        List[str]. Lista com os nomes das ações cujo preço atingiu ou
        ultrapassou o valor_alvo entre o valor anterior e o valor atual.
    """
    # Setando a seed para reprodutibilidade
    random.seed(42)

    # Inicializa a lista de ações atingidas
    acoes_atingidas = []

    # Lock para garantir acesso seguro à lista compartilhada
    lock = threading.Lock()

    # Lista para armazenar as threads
    threads = []

    # Função executada por cada thread para monitorar uma única ação.
    def _worker_monitorar_acao(acao: str):
        # Simula um atraso de rede para obter o primeiro preço
        time.sleep(random.uniform(0.1, 0.5))
        # Gera um valor de preço "anterior" aleatório
        valor_anterior = random.uniform(99, 101)

        # Simula outro atraso de rede para obter o preço atualizado
        time.sleep(random.uniform(0.2, 0.8))
        # Gera um valor "atual" com uma pequena variação do anterior
        variacao = random.uniform(0.95, 1.05)
        valor_atual = valor_anterior * variacao

        # Verifica se o valor_alvo foi atingido no intervalo de preços
        preco_min = min(valor_anterior, valor_atual)
        preco_max = max(valor_anterior, valor_atual)

        if preco_min <= valor_alvo <= preco_max:
            print(
                f"Ação {acao} atingiu o valor alvo: {valor_alvo}"
                f" (Anterior: {valor_anterior:.2f}, Atual: {valor_atual:.2f})"
            )
            # Lock para garantir acesso exclusivo à lista compartilhada
            with lock:
                acoes_atingidas.append(acao)
        else:
            print(
                f"Ação {acao} não atingiu o valor alvo: {valor_alvo}"
                f" (Anterior: {valor_anterior:.2f}, Atual: {valor_atual:.2f})"
            )

    # Cria e inicia uma thread para cada ação na lista de entrada
    for acao in acoes:
        thread = threading.Thread(target=_worker_monitorar_acao, args=(acao,))
        threads.append(thread)
        thread.start()

    # Espera que todas as threads terminem sua execução
    for thread in threads:
        thread.join()

    return acoes_atingidas
