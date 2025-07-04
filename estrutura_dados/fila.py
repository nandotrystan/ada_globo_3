class Fila:
    """
    Implementação de uma fila simples usando lista.
    A fila é uma estrutura de dados do tipo FIFO (First In, First Out),
    onde os elementos são adicionados no final e removidos do início.
    Esta classe permite enfileirar (adicionar) e desenfileirar (remover) itens,
    além de verificar se a fila está vazia e obter o tamanho da fila.

    """
    def __init__(self):
        self.itens = []

    def esta_vazia(self):
        return len(self.itens) == 0

    def enfileirar(self, item):
        self.itens.append(item)

    def desenfileirar(self):
        if not self.esta_vazia():
            return self.itens.pop(0)
        raise IndexError("Desenfileirar de uma fila vazia")

    def tamanho(self):
        return len(self.itens)

    def __str__(self):
        return str(self.itens)


from collections import deque

class FilaCSV:
    """
    Implementação de uma fila para manipulação de linhas CSV.
    Esta classe utiliza a deque do módulo collections para
    permitir operações eficientes de enfileiramento e desenfileiramento.
    A fila é usada para armazenar linhas de um arquivo CSV, permitindo
    que as linhas sejam processadas na ordem em que foram lidas.
    
    """
    def __init__(self):
        self.fila = deque()

    def enfileirar(self, linha_csv):
        self.fila.append(linha_csv)

    def desenfileirar(self):
        if not self.esta_vazia():
            return self.fila.popleft()
        return None

    def esta_vazia(self):
        return len(self.fila) == 0