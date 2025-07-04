## Algoritmos de ordenação

# Algoritmos de ordenação são fundamentais em ciência da computação e são usados para organizar dados de maneira eficiente. Existem vários algoritmos de ordenação, cada um com suas características, vantagens e desvantagens. Aqui estão alguns dos mais comuns:
# Bubble sort é um algoritmo de ordenação simples que funciona repetidamente passando pela lista, comparando elementos adjacentes e trocando-os se estiverem na ordem errada. É um algoritmo ineficiente para listas grandes, mas fácil de entender e implementar.
# É um algoritmo in-place, o que significa que não requer espaço adicional significativo.
def bubble_sort(arr):
    n = len(arr)    
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
# Insertion sort é um algoritmo de ordenação simples que constrói a lista ordenada um elemento de cada vez. Ele é mais eficiente em listas pequenas ou quase ordenadas.
# É um algoritmo in-place, o que significa que não requer espaço adicional significativo.
# def insertion_sort(arr):
#     for i in range(1, len(arr)):
#         key = arr[i]
#         j = i-1
#         while j >= 0 and key < arr[j]:
#             arr[j + 1] = arr[j]
#             j -= 1
#         arr[j + 1] = key
#     return arr  

def insertion_sort(arr, chave_metrica=None, key_func=None, reverso=False):
    def obter_valor(obj):
        if key_func:
            return key_func(obj)
        if chave_metrica:
            attr = getattr(obj, chave_metrica)
            return attr() if callable(attr) else attr
        return obj  # fallback: compara o próprio objeto

    for i in range(1, len(arr)):
        atual = arr[i]
        chave_atual = obter_valor(atual)
        j = i - 1

        while j >= 0 and (
            obter_valor(arr[j]) > chave_atual if reverso else obter_valor(arr[j]) < chave_atual
        ):
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = atual
    return arr

# 
# def quick_sort(arr):
#     if len(arr) <= 1:
#         return arr
#     print("arr", arr)
#     pivot = arr[len(arr) // 2]
#     print("pivot", pivot)
#     left = [x for x in arr if x < pivot]
#     print("left", left)
#     middle = [x for x in arr if x == pivot]
#     print("middle", middle)
#     right = [x for x in arr if x > pivot]
#     print("right", right)
    
#     # print("quick_sort", quick_sort(left.copy()), middle, quick_sort(right.copy()))
#     return quick_sort(left) + middle + quick_sort(right)

# Quick sort é um algoritmo de ordenação eficiente que utiliza a técnica de divisão e conquista. Ele escolhe um "pivô" e particiona o array em dois sub-arrays, um com elementos menores que o pivô e outro com elementos maiores.
# É um algoritmo in-place, o que significa que não requer espaço adicional significativo, exceto para a pilha de chamadas recursivas.
def quick_sort(arr, chave_metrica=None, key_func=None):
    if len(arr) <= 1:
        return arr

    def obter_valor(obj):
        if key_func:
            return key_func(obj)
        elif chave_metrica:
            attr = getattr(obj, chave_metrica)
            return attr() if callable(attr) else attr
        else:
            return obj  # comparação direta (ex: números)

    pivot = arr[len(arr) // 2]
    pivot_val = obter_valor(pivot)

    left = [x for x in arr if obter_valor(x) > pivot_val]    # decrescente
    middle = [x for x in arr if obter_valor(x) == pivot_val]
    right = [x for x in arr if obter_valor(x) < pivot_val]

    return quick_sort(left, chave_metrica, key_func) + middle + quick_sort(right, chave_metrica, key_func)



def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def merge_sort(arr, chave_metrica=None, key_func=None):
    if len(arr) <= 1:
        return arr

    def obter_valor(obj):
        if key_func:
            return key_func(obj)
        elif isinstance(chave_metrica, str):
            attr = getattr(obj, chave_metrica)
            return attr() if callable(attr) else attr
        else:
            raise ValueError("Você deve fornecer 'key_func' ou 'chave_metrica' válida.")

    def merge(left, right):
        resultado = []
        i = j = 0
        while i < len(left) and j < len(right):
            if obter_valor(left[i]) > obter_valor(right[j]):  # ordem decrescente
                resultado.append(left[i])
                i += 1
            else:
                resultado.append(right[j])
                j += 1
        resultado.extend(left[i:])
        resultado.extend(right[j:])
        return resultado

    meio = len(arr) // 2
    esquerda = merge_sort(arr[:meio], chave_metrica, key_func)
    direita = merge_sort(arr[meio:], chave_metrica, key_func)
    return merge(esquerda, direita)

# def merge_sort(arr):
#     if len(arr) > 1:
#         mid = len(arr) // 2
#         L = arr[:mid]
#         R = arr[mid:]

#         merge_sort(L)
#         merge_sort(R)

#         i = j = k = 0

#         while i < len(L) and j < len(R):
#             if L[i] < R[j]:
#                 arr[k] = L[i]
#                 i += 1
#             else:
#                 arr[k] = R[j]
#                 j += 1
#             k += 1

#         while i < len(L):
#             arr[k] = L[i]
#             i += 1
#             k += 1

#         while j < len(R):
#             arr[k] = R[j]
#             j += 1
#             k += 1

#     return arr






