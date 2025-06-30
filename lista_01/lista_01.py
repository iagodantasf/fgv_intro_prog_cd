from typing import List, Tuple, Any, Dict


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


# 5. Alisamento de Lista Aninhada
def flatten(lst: List[Any]) -> List[Any]:
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list


# Parte 2: Dicionários


# 1. Agrupamento por Chave
def group_by(pairs: List[Tuple[Any, Any]]) -> Dict[Any, List[Any]]:
    result = {}
    for tpl in pairs:
        key, value = tpl
        if key not in result:
            result[key] = []
        result[key].append(value)
    return result


# 2. Inversão de Mapeamento
def invert_map(d: Dict[Any, Any]) -> Dict[Any, Any]:
    inverted = {}
    for key, value in d.items():
        if value not in inverted:
            inverted[value] = key
        else:
            raise ValueError(f"Valor duplicado encontrado: {value}")
    return inverted


# 3. Índices por Valor
def indices_of(lst: List[Any]) -> Dict[Any, List[int]]:
    idx = {}
    for i, value in enumerate(lst):
        if value not in idx:
            idx[value] = []
        idx[value].append(i)
    return idx


# 4. Fusão com Resolução de Conflitos
def merge_dicts(dicts: List[Dict[Any, Any]]) -> Dict[Any, Any]:
    merged = {}
    for d in dicts:
        for key, value in d.items():
            if key in merged:
                merged[key] += value
            else:
                merged[key] = value
    return merged


# 5. Contador de Dígitos
def conta_digitos(n: int) -> Dict[int, int]:
    n = abs(n)  # Considera o valor absoluto
    # Inicializa o dicionário com contagem zero:
    digit_count = dict((zip(range(10), [0] * 10)))
    for digit in str(n):
        digit = int(digit)
        digit_count[digit] += 1
    return digit_count


# Parte 3: Desafios de Funções


# 1. Contador de Anagramas
def count_anagrams(words: List[str]) -> Dict[str, List[str]]:
    anagrams = {}
    for word in words:
        sorted_word = ''.join(sorted(word))
        if sorted_word not in anagrams:
            anagrams[sorted_word] = []
        anagrams[sorted_word].append(word)
    return anagrams


# 2. Parser de CSV
def parse_csv(text: str, sep: str = ", ") -> Dict[str, List[str]]:
    lines = text.strip().split("\n")
    headers = lines[0].split(sep)
    data = {header: [] for header in headers}
    for line in lines[1:]:
        values = line.split(sep)
        for header, value in zip(headers, values):
            if all(c in "0123456789" for c in value):
                value = int(value)
            data[header].append(value)
    return data


# 3. Validação de Sudoku
def validar_sudoku(tabuleiro: List[List[int]]) -> bool:
    def is_valid_group(group: List[int]) -> bool:
        occ = {n: 0 for n in range(1, 10)}
        for num in group:
            if num != 0:
                occ[num] += 1
                if occ[num] > 1:
                    return False
        return True
    # Verifica linhas e colunas
    for i in range(9):
        if (
            not is_valid_group(tabuleiro[i])
            or not is_valid_group([tabuleiro[j][i] for j in range(9)])
        ):
            return False
    # Verifica submatrizes 3x3
    for i in range(3):
        for j in range(3):
            subgrid = [
                tabuleiro[x][y]
                for x in range(i * 3, (i + 1) * 3)
                for y in range(j * 3, (j + 1) * 3)
            ]
            if not is_valid_group(subgrid):
                return False
    return True
