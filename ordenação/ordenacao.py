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


# def quick_sort(arr, chave_metrica):
#     if len(arr) <= 1:
#         return arr

#     def obter_valor(obj):
#         attr = getattr(obj, chave_metrica)
#         return attr() if callable(attr) else attr

#     pivot = arr[len(arr) // 2]
#     pivot_val = obter_valor(pivot)

#     left = [x for x in arr if obter_valor(x) > pivot_val]  # > para ordem decrescente
#     middle = [x for x in arr if obter_valor(x) == pivot_val]
#     right = [x for x in arr if obter_valor(x) < pivot_val]

#     return quick_sort(left, chave_metrica) + middle + quick_sort(right, chave_metrica)

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




def counting_sort(arr):
    if len(arr) == 0:
        return arr

    max_val = max(arr)
    count = [0] * (max_val + 1)

    for num in arr:
        count[num] += 1

    sorted_arr = []
    for i in range(len(count)):
        sorted_arr.extend([i] * count[i])

    return sorted_arr

def bucket_sort(arr):
    if len(arr) == 0:
        return arr

    max_val = max(arr)
    bucket_count = len(arr)
    buckets = [[] for _ in range(bucket_count)]

    for num in arr:
        index = int(num * bucket_count / (max_val + 1))
        buckets[index].append(num)

    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(sorted(bucket))

    return sorted_arr

def shell_sort(arr):
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2

    return arr

def cocktail_sort(arr):
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1

    while swapped:
        swapped = False

        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        if not swapped:
            break

        swapped = False
        end -= 1

        for i in range(end, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        start += 1

    return arr

def gnome_sort(arr):
    index = 0
    n = len(arr)

    while index < n:
        if index == 0 or arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1

    return arr

def comb_sort(arr):
    n = len(arr)
    gap = n
    shrink = 1.3
    sorted = False

    while not sorted:
        gap = int(gap / shrink)
        if gap < 1:
            gap = 1
        sorted = True

        for i in range(n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False

    return arr

def tim_sort(arr): 
    min_run = 32
    n = len(arr)

    def insertion_sort(sub_arr):
        for i in range(1, len(sub_arr)):
            key = sub_arr[i]
            j = i - 1
            while j >= 0 and key < sub_arr[j]:
                sub_arr[j + 1] = sub_arr[j]
                j -= 1
            sub_arr[j + 1] = key

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    size = 1
    while size < n:
        for start in range(0, n, size * 2):
            mid = min(start + size, n)
            end = min(start + size * 2, n)
            left = arr[start:mid]
            right = arr[mid:end]
            insertion_sort(left)
            insertion_sort(right)
            arr[start:end] = merge(left, right)
        size *= 2

    return arr

def flash_sort(arr):
    n = len(arr)
    if n == 0:
        return arr

    max_val = max(arr)
    min_val = min(arr)
    m = int(n * 0.43)
    if m < 2:
        m = 2

    buckets = [0] * m
    for num in arr:
        index = int((num - min_val) / (max_val - min_val) * (m - 1))
        buckets[index] += 1

    for i in range(1, m):
        buckets[i] += buckets[i - 1]

    temp = arr[:]
    for i in range(n):
        index = int((temp[i] - min_val) / (max_val - min_val) * (m - 1))
        while i < buckets[index]:
            buckets[index] -= 1
            arr[buckets[index]] = temp[i]
            i += 1

    return arr

def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

    return arr

