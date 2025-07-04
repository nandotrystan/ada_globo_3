# 2.2. Gerenciamento de Conteúdos e Usuários (Árvore de Busca Binária)
# Para gerenciar os objetos Conteudo e Usuario, utilize Árvores de Busca Binária (Binary Search Trees - BSTs). Isso permitirá uma busca, inserção e remoção mais eficiente em comparação com listas lineares, especialmente à medida que o número de conteúdos e usuários cresce.

# 2.2.1. Árvore de Conteúdos
# Chave da BST: _id_conteudo (inteiro)

# Operações:

# inserir_conteudo(conteudo): Adiciona um objeto Conteudo à árvore, utilizando o _id_conteudo como chave.
# buscar_conteudo(id_conteudo): Retorna o objeto Conteudo correspondente ao id_conteudo fornecido, ou None se não encontrado.
# remover_conteudo(id_conteudo): Remove o conteúdo da árvore.
# percurso_em_ordem(): Retorna uma lista de todos os conteúdos na árvore em ordem crescente de _id_conteudo.
# 2.2.2. Árvore de Usuários
# Chave da BST: _id_usuario (inteiro)

# Operações:

# inserir_usuario(usuario): Adiciona um objeto Usuario à árvore, utilizando o _id_usuario como chave.
# buscar_usuario(id_usuario): Retorna o objeto Usuario correspondente ao id_usuario fornecido, ou None se não encontrado.
# remover_usuario(id_usuario): Remove o usuário da árvore.
# percurso_em_ordem(): Retorna uma lista de todos os usuários na árvore em ordem crescente de _id_usuario.

from entidades.conteudo import Conteudo

class Node:
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