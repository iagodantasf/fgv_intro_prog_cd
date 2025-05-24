from typing import List, Tuple, Any


# Parte 1: Listas e Tuplas


# 1. Números Pares e Ímpares
def pares_e_impares(nums: List[int]) -> Tuple[List[int], List[int]]:
    pares = [num for num in nums if num % 2 == 0]
    impares = [num for num in nums if num % 2 != 0]
    return pares, impares


# 2. Filtrar por Comprimento
def filtrar_por_tamanho(lista: List[str], k: int) -> List[str]:
    return [item for item in lista if len(item) > k]


# 3. Rotação de Tupla
def rotate_tuple(tpl: Tuple[Any, ...], n: int) -> Tuple[Any, ...]:
    n = n % len(tpl)  # Para evitar rotações desnecessárias
    return tpl[-n:] + tpl[:-n]


# 4. Transposta de Matriz
def transpose(matrix: List[List[Any]]) -> List[List[Any]]:
    return [list(row) for row in zip(*matrix)]
