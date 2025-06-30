import math
import itertools
import random
import urllib
import os
from typing import List, Tuple, Any, Iterable
from tqdm import tqdm


# Parte 1: Biblioteca math


# 1. Valor Futuro (Juros Compostos)
def future_value(pv: float, r: float, n: int, t: float) -> float:
    """
    Calcula o valor futuro de um investimento com juros compostos.

    Args:
        pv (float): Valor presente (capital inicial).
        r (float): Taxa de juros anual (em decimal).
        n (int): Número de vezes que os juros são compostos por ano.
        t (float): Tempo em anos.

    Returns:
        float: Valor futuro do investimento.
    """
    return pv * math.pow((1 + r / n), n * t)  # ou pv * (1 + r / n) ** (n * t)


# 2. Desvio Padrão de Retornos
def standard_deviation(returns: List[float]) -> float:
    """
    Calcula o desvio padrão de uma lista de retornos.

    Args:
        returns (List[float]): Lista de retornos.

    Returns:
        float: Desvio padrão dos retornos.
    """
    n = len(returns)
    if n == 0:
        raise ValueError("A lista de retornos não pode estar vazia.")
    mean = sum(returns) / n
    variance = sum((x - mean)**2 for x in returns) / n
    return math.sqrt(variance)


# 3. Tempo para Dobrar (Capitalização Contínua)
def time_to_double(r: float) -> float:
    """
    Calcula o tempo necessário para dobrar um investimento com
    capitalização contínua.

    Args:
        r (float): Taxa de juros anual (em decimal).

    Returns:
        float: Tempo necessário para dobrar o investimento (em anos).
    """
    if r <= 0:
        raise ValueError("A taxa de juros deve ser maior que zero.")
    return math.log(2) / math.log(1 + r)


# Parte 2: Biblioteca itertools


# 1. Combinações de Ativos
def portfolio_combinations(assets: List[str], k: int) -> List[Tuple[str, ...]]:
    """
    Gera todas as combinações possíveis de k ativos de uma lista de ativos.

    Args:
        assets (List[str]): Lista de nomes dos ativos.
        k (int): Número de ativos em cada combinação.

    Returns:
        List[Tuple[str, ...]]: Lista de combinações possíveis.
    """
    if k < 0 or k > len(assets):
        raise ValueError("k deve estar entre 0 e o número total de ativos.")
    return list(itertools.combinations(assets, k))


# 2. Média Móvel
def moving_average(prices: List[float], window: int) -> List[float]:
    """
    Calcula a média móvel de uma lista de preços.

    Args:
        prices (List[float]): Lista de preços.
        window (int): Tamanho da janela para a média móvel.

    Returns:
        List[float]: Lista de médias móveis.
    """
    if window <= 0:
        raise ValueError("O tamanho da janela deve ser maior que zero.")
    if not prices:
        raise ValueError("A lista de preços não pode estar vazia.")
    if window > len(prices):
        raise ValueError(
            "O tamanho da janela não pode ser maior que o tamanho da lista."
        )

    def rolling_window(
        iterable: Iterable,
        n: int,
    ) -> Iterable[Tuple[Any, ...]]:
        """
        Gera janelas deslizantes de tamanho n a partir de um iterável.

        Args:
            iterable (Iterable): Iterável de onde as janelas serão geradas.
            n (int): Tamanho da janela.

        Yields:
            Iterable[Tuple[Any, ...]]: Janelas deslizantes de tamanho n.
        """
        it = iter(iterable)
        window = tuple(itertools.islice(it, n))
        if len(window) == n:
            yield window
        for elem in it:
            window = window[1:] + (elem,)
            yield window

    return [
        sum(_rolling_window) / window
        for _rolling_window in rolling_window(prices, window)
    ]


# Parte 3: Biblioteca random


# 1. Simulação de Preço de Ação
def simulate_stock_price(
    initial_price: float,
    mu: float,
    sigma: float,
    days: int,
) -> List[float]:
    """
    Simula o preço de uma ação por um determinado número de dias.

    Args:
        initial_price (float): Preço inicial da ação.
        mu (float): Média das variações diárias.
        sigma (float): Desvio padrão das variações diárias.
        days (int): Número de dias para simulação.

    Returns:
        List[float]: Lista de preços simulados da ação ao longo dos dias.
    """
    # Configurando a seed para reprodutibilidade
    random.seed(0)

    # Simulação do preço da ação
    prices = [initial_price]
    for _ in range(days):
        variation = random.gauss(mu, sigma)
        new_price = prices[-1] + variation
        prices.append(new_price)
    return prices


# Parte 4: Bibliotecas urllib e os


# 1. Download e Concatenação de Dados do BLS QCEW
def download_and_merge(
    years_quarters: List[Tuple[int, int]],
    output_file: str,
) -> None:
    """
    Baixa dados do BLS QCEW para diferentes trimestres e anos e os
    concatena em um único arquivo CSV.

    Args:
        years_quarters (List[Tuple[int, int]]): Lista de tuplas com ano
        e trimestre.
        output_file (str): Caminho do arquivo CSV de saída.

    Returns:
        None
    """
    # Cria o diretório data/ se não existir
    if not os.path.exists("data"):
        os.makedirs("data")

    # Lista para armazenar os caminhos dos arquivos baixados
    downloaded_files = []

    for year, quarter in tqdm(
        years_quarters,
        desc="Baixando os arquivos do BLS QCEW",
    ):
        url = (
            "https://data.bls.gov/cew/data/api/"
            f"{year}/{quarter}/industry/10.csv"
        )
        file_path = f"data/{year}_q{quarter}.csv"
        # Baixa o arquivo
        urllib.request.urlretrieve(url, file_path)
        downloaded_files.append(file_path)

    # Lista todos os arquivos baixados ordenados pelo nome
    downloaded_files.sort()
    print("Arquivos baixados:")
    for file_ in downloaded_files:
        print(file_)

    # Gerando o output_file
    with open(output_file, "w", encoding="utf-8") as outfile:
        header_written = False
        for file_path in downloaded_files:
            with open(file_path, "r", encoding="utf-8") as infile:
                infile = list(infile)
                if not header_written:
                    # Escreve o cabeçalho do primeiro arquivo
                    header = infile[0]
                    outfile.write(header)
                    header_written = True
                for line in infile[1:]:
                    # Escreve as linhas de dados (sem cabeçalho)
                    outfile.write(line)
