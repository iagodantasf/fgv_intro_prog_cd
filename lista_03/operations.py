import numpy as np


# Parte 2: Operações em Vetores e Matrizes


# 1. Rotação de Matriz 90˚ no Sentido Horário
def rotate_90(A: np.ndarray) -> np.ndarray:
    """
    Rotaciona uma matriz quadrada 90 graus no sentido horário.

    Args:
        A (np.ndarray): Matriz quadrada de formato (n, n).

    Returns:
        np.ndarray: Matriz rotacionada de formato (n, n).
    """
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A matriz deve ser quadrada (n x n).")

    def transpose(matrix: np.ndarray) -> np.ndarray:
        """
        Transpõe uma matriz (troca linhas por colunas).

        Args:
            matrix (np.ndarray): Matriz a ser transposta.

        Returns:
            np.ndarray: Matriz transposta.
        """
        rows, cols = matrix.shape

        # Inicializando a matriz transposta
        transposed = np.empty((cols, rows), dtype=matrix.dtype)

        # Preenchendo a matriz transposta
        for i in range(rows):
            for j in range(cols):
                transposed[j, i] = matrix[i, j]

        return transposed

    # Transpondo a matriz A
    A_t = transpose(A)

    # Invertendo a ordem das colunas de A_t
    A_rot = np.empty_like(A_t)
    for i in range(A_t.shape[0]):
        A_rot[i] = A_t[i][::-1]

    return A_rot


# 2. Soma de Subdiagonais de uma Matriz
def sum_subdiagonals(A: np.ndarray, k: int) -> float:
    """
    Soma os elementos de uma subdiagonal de uma matriz.

    Args:
        A (np.ndarray): Matriz de formato (m, n).
        k (int): Índice da subdiagonal a ser somada.
                 k = 0 para a diagonal principal,
                 k > 0 para subdiagonais abaixo da principal,
                 k < 0 para subdiagonais acima da principal.

    Returns:
        float: Soma dos elementos da subdiagonal.
    """
    if A.ndim != 2:
        raise ValueError("A matriz deve ser bidimensional (m x n).")

    # Número de linhas e colunas da matriz
    m, n = A.shape

    # Inicializando a soma
    total = 0.0

    # Acrescentando os elementos da subdiagonal na soma
    for i in range(m):
        j = i - k
        if 0 <= j < n:
            total += A[i, j]

    return total


# 3. Multiplicação de Matrizes em Blocos
def block_mat_mul(A: np.ndarray, B: np.ndarray, block_size: int) -> np.ndarray:
    """
    Multiplica duas matrizes usando multiplicação em blocos.

    Args:
        A (np.ndarray): Matriz de formato (m, p).
        B (np.ndarray): Matriz de formato (p, n).
        block_size (int): Tamanho do bloco para a multiplicação.

    Returns:
        np.ndarray: Matriz resultante de formato (m, n).
    """
    # Verificando os formatos das matrizes e o tamanho do bloco
    if A.ndim != 2 or B.ndim != 2:
        raise ValueError(
            "As matrizes A e B devem ser bidimensionais (m x p e p x n)."
        )
    if A.shape[1] != B.shape[0]:
        raise ValueError(
            "O número de colunas de A deve ser igual ao número de linhas de B."
        )
    if block_size <= 0:
        raise ValueError("O tamanho do bloco deve ser maior que zero.")

    # Obtendo as dimensões das matrizes A e B
    m, p = A.shape
    n = B.shape[1]

    # Inicializando a matriz resultante
    C = np.zeros((m, n), dtype=A.dtype)

    # Iterando sobre os blocos
    for i in range(0, m, block_size):
        for j in range(0, n, block_size):
            for k in range(0, p, block_size):

                # Definindo os limites dos blocos
                i_end = min(i + block_size, m)
                j_end = min(j + block_size, n)
                k_end = min(k + block_size, p)

                # Multiplicando os blocos
                C[i: i_end, j: j_end] += (
                    A[i: i_end, k: k_end] @ B[k: k_end, j: j_end]
                )
    return C
