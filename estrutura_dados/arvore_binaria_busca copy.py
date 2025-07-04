from entidades.conteudo import Conteudo

class Node:
    """
    Classe que representa um nó em uma árvore binária de busca (BST).
    Cada nó contém uma chave, um objeto (instância de Conteudo), e referências para os nós filhos esquerdo e direito.
    A chave é usada para organizar os nós na árvore, permitindo operações de inserção, busca
    e remoção de forma eficiente.
    A classe também implementa métodos para representar o nó como string e para exibir suas informações.
    A classe BST (Binary Search Tree) é usada para gerenciar a árvore, permitindo inserir
    e buscar nós com base em suas chaves.
    A classe BST também permite percorrer a árvore em ordem, retornando uma lista de objetos
    associados aos nós na ordem correta.
    A classe Node é essencial para a construção de uma árvore binária de busca, onde cada nó
    pode ter até dois filhos, e a organização dos nós permite operações eficientes de busca e manipulação.
    A classe BST é responsável por gerenciar a estrutura da árvore, permitindo a inserção,
    busca e remoção de nós, além de percorrer a árvore em ordem.
    A classe Node é usada internamente pela classe BST para representar cada nó da árvore.
    """
    def __init__(self, chave, objeto):
        self.chave = chave
        self.objeto = objeto
        self.esquerda = None
        self.direita = None

    def __repr__(self):
        return f"Node(chave={self.chave}, objeto={self.objeto})"
    
    def __str__(self):
        self.chave = self.chave if isinstance(self.chave, int) else str(self.chave)
        self.objeto = self.objeto if isinstance(self.objeto, Conteudo) else str(self.objeto)
        self.esquerda = self.esquerda if self.esquerda is None else str(self.esquerda.chave)
        self.direita = self.direita if self.direita is None else str(self.direita.chave)
        return f"Node(chave={self.chave}, objeto={self.objeto})"

class BST:
    def __init__(self):
        self.raiz = None

    def inserir(self, chave, objeto):
        self.raiz = self._inserir(self.raiz, chave, objeto)

    def _inserir(self, no, chave, objeto):
        if no is None:
            return Node(chave, objeto)
        if chave < no.chave:
            no.esquerda = self._inserir(no.esquerda, chave, objeto)
        elif chave > no.chave:
            no.direita = self._inserir(no.direita, chave, objeto)
        return no

    def buscar(self, chave):
        return self._buscar(self.raiz, chave)

    def _buscar(self, no, chave):
        if no is None:
            return None
        if chave == no.chave:
            return no.objeto
        elif chave < no.chave:
            return self._buscar(no.esquerda, chave)
        else:
            return self._buscar(no.direita, chave)

    def remover(self, chave):
        self.raiz = self._remover(self.raiz, chave)

    def _remover(self, no, chave):
        if no is None:
            return None
        if chave < no.chave:
            no.esquerda = self._remover(no.esquerda, chave)
        elif chave > no.chave:
            no.direita = self._remover(no.direita, chave)
        else:
            # Nó com um ou nenhum filho
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda
            # Nó com dois filhos
            sucessor = self._minimo(no.direita)
            no.chave, no.objeto = sucessor.chave, sucessor.objeto
            no.direita = self._remover(no.direita, sucessor.chave)
        return no

    def _minimo(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def percurso_em_ordem(self):
        resultado = []
        self._em_ordem(self.raiz, resultado)
        return resultado

    def _em_ordem(self, no, resultado):
        if no is not None:
            self._em_ordem(no.esquerda, resultado)
            resultado.append(no.objeto)
            self._em_ordem(no.direita, resultado)
    
    


# class No:
#     def __init__(self, conteudo):
#         self.conteudo = conteudo
#         self.esquerda = None
#         self.direita = None

# class ArvoreBinariaBusca:
#     def __init__(self):
#         self.raiz = None

#     def inserir(self, conteudo):
#         if not isinstance(conteudo, Conteudo):
#             raise TypeError("O conteúdo deve ser uma instância da classe Conteudo")
#         self.raiz = self._inserir_recursivo(self.raiz, conteudo)

#     def _inserir_recursivo(self, no, conteudo):
#         if no is None:
#             return No(conteudo)
#         if conteudo._id_conteudo < no.conteudo._id_conteudo:
#             no.esquerda = self._inserir_recursivo(no.esquerda, conteudo)
#         elif conteudo._id_conteudo > no.conteudo._id_conteudo:
#             no.direita = self._inserir_recursivo(no.direita, conteudo)
#         return no

#     def buscar(self, id_conteudo):
#         return self._buscar_recursivo(self.raiz, id_conteudo)

#     def _buscar_recursivo(self, no, id_conteudo):
#         if no is None or no.conteudo._id_conteudo == id_conteudo:
#             return no.conteudo if no else None
#         if id_conteudo < no.conteudo._id_conteudo:
#             return self._buscar_recursivo(no.esquerda, id_conteudo)
#         return self._buscar_recursivo(no.direita, id_conteudo)

#     def remover(self, id_conteudo):
#         self.raiz = self._remover_recursivo(self.raiz, id_conteudo)

#     def _remover_recursivo(self, no, id_conteudo):
#         if no is None:
#             return no
#         if id_conteudo < no.conteudo._id_conteudo:
#             no.esquerda = self._remover_recursivo(no.esquerda, id_conteudo)
#         elif id_conteudo > no.conteudo._id_conteudo:
#             no.direita = self._remover_recursivo(no.direita, id_conteudo)
#         else:
#             # Nó com apenas um filho ou nenhum filho
#             if no.esquerda is None:
#                 return no.direita
#             elif no.direita is None:
#                 return no.esquerda