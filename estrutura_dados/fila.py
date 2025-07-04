class Fila:
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