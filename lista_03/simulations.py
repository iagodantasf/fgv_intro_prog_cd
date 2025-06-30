import numpy as np


# Parte 1: Simulação de Preços e Análise de Retornos


# 1. Simulação de Série de Preços com Ruído Gaussiano
def simular_precos(S0: float, sigma: float, days: int) -> np.ndarray:
    """
    Simula uma série temporal de preços de ações com ruído gaussiano.

    Args:
        S0 (float): Preço inicial da ação.
        sigma (float): Desvio padrão do ruído (volatilidade).
        days (int): Número de dias a simular.

    Returns:
        np.ndarray: Série temporal de preços simulados.
    """
    # Validações de entrada
    if S0 <= 0:
        raise ValueError("O preço inicial deve ser positivo.")
    if sigma < 0:
        raise ValueError("O desvio padrão não pode ser negativo.")
    if days < 0:
        raise ValueError("O número de dias não pode ser negativo.")

    # Configurando a seed para reprodutibilidade
    np.random.seed(42)

    # Simulação de preços
    prices = [S0]
    for _ in range(days):
        noise = np.random.normal(0, sigma)
        prices.append(prices[-1] + noise)

    return np.array(prices)


# 2. Cálculo de Retornos Simples e Logarítmicos
def calc_retornos_simples(prices: np.ndarray) -> np.ndarray:
    """
    Calcula os retornos simples diários a partir de uma série de preços.

    Args:
        prices (np.ndarray): Vetor de preços.

    Returns:
        np.ndarray: Vetor de retornos simples.
    """
    if len(prices) < 2:
        raise ValueError(
            "O vetor de preços deve ter pelo menos dois elementos."
        )

    return np.diff(prices) / prices[: -1]


def calc_retornos_log(prices: np.ndarray) -> np.ndarray:
    """
    Calcula os log-retornos diários a partir de uma série de preços.

    Args:
        prices (np.ndarray): Vetor de preços.

    Returns:
        np.ndarray: Vetor de log-retornos.
    """
    if len(prices) < 2:
        raise ValueError(
            "O vetor de preços deve ter pelo menos dois elementos."
        )

    return np.log(prices[1:] / prices[:-1])


# 3. Indicadores Móveis: Média e Volatilidade
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


def rolling_std(
    returns: np.ndarray,
    window: int,
    days_size: int = 0,
) -> np.ndarray:
    """
    Calcula o desvio padrão móvel para um vetor de retornos.

    Args:
        returns (np.ndarray): Vetor de retornos.
        window (int): Tamanho da janela para o desvio padrão.
        days_size (int, optional): Ajuste para a normalização. Default é 0.

    Returns:
        np.ndarray: Vetor de desvios padrão móveis.
    """
    if window <= 0:
        raise ValueError("O tamanho da janela deve ser maior que zero.")
    if len(returns) < window:
        raise ValueError(
            "O vetor de retornos deve ter pelo menos 'window' elementos."
        )

    # Calcula a média móvel
    sma_values = sma(returns, window)

    # Calcula o desvio padrão móvel
    sum_squared_diff = np.zeros(len(returns) - window + 1)
    for i in range(len(sum_squared_diff)):
        sum_squared_diff[i] = np.sum(
            (returns[i: i + window] - sma_values[i]) ** 2
        )

    # Tirando a média normalizada e a e raiz quadrada
    return np.sqrt(sum_squared_diff / (window - days_size))
