import numpy as np
from copy import copy
from typing import Tuple


# Parte 3: Filtragem e Picos


# 1. Substituição Condicional em Vetores
def replace_negatives(v: np.ndarray, new_value: float) -> np.ndarray:
    """
    Substitui todos os valores negativos do vetor v por new_value.

    Args:
        v (np.ndarray): Vetor de entrada.
        new_value (float): Valor para substituir os negativos.

    Returns:
        np.ndarray: Vetor com os valores negativos substituídos.
    """
    # Criando uma cópia do vetor para evitar modificar o original
    v = copy(v)

    # Substituindo os valores negativos
    v[v < 0] = new_value

    return v


# 2. Identificação de Máximos Locais em Série Temporal
def local_peaks(series: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Identifica os picos locais em uma série temporal.

    Args:
        series (np.ndarray): Série temporal de entrada.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Índices e valores dos picos locais.
    """
    # Verificando se a série tem pelo menos 3 elementos
    if len(series) < 3:
        return np.array([]), np.array([])

    # Inicializando listas para os índices e valores dos picos
    peaks_indices = []
    peaks_values = []

    # Iterando sobre a série para encontrar picos locais
    for i in range(1, len(series) - 1):
        if (series[i] > series[i - 1]) and (series[i] > series[i + 1]):
            peaks_indices.append(i)
            peaks_values.append(series[i])

    # Convertendo listas para arrays numpy
    peaks_indices = np.array(peaks_indices) + 1  # de 1 a N
    peaks_values = np.array(peaks_values)

    return peaks_indices, peaks_values
