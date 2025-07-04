class NodeAVL:
    """
    Classe que representa um nó em uma árvore AVL.
    Cada nó contém uma chave, um objeto (instância de Conteudo), e referências para os nós filhos esquerdo e direito.
    A chave é usada para organizar os nós na árvore, permitindo operações de inserção, busca
    e remoção de forma eficiente.
    A classe também implementa métodos para calcular a altura do nó e o fator de balanceamento
    (diferença entre as alturas dos subárvores esquerda e direita).
    A classe NodeAVL é essencial para a construção de uma árvore AVL, onde cada nó pode ter até dois filhos,
    e a organização dos nós permite operações eficientes de busca e manipulação, mantendo a árvore balanceada.
    A classe AVLTree é responsável por gerenciar a estrutura da árvore AVL, permitindo a inserção,
    busca e remoção de nós, além de percorrer a árvore em ordem.
    A classe NodeAVL é usada internamente pela classe AVLTree para representar cada nó da árvore.   

    """
    def __init__(self, chave, objeto):
        self.chave = chave
        self.objeto = objeto
        self.esquerda = None
        self.direita = None
        self.altura = 1

class AVLTree:
    """
    Classe que representa uma árvore AVL (Adelson-Velsky e Landis).
    A árvore AVL é uma árvore binária de busca balanceada, onde a diferença de alturas entre as subárvores esquerda e direita de qualquer nó é no máximo 1.
    A classe permite inserir nós, buscar por chaves, e percorrer a árvore em ordem.
    Cada nó é representado pela classe NodeAVL, que contém uma chave, um objeto (instância de Conteudo), e referências para os nós filhos esquerdo e direito.
    A classe AVLTree implementa as operações de inserção com balanceamento automático, garantindo que a árvore permaneça balanceada após cada inserção.
    A classe também implementa métodos para calcular a altura do nó e o fator de balanceamento
    (diferença entre as alturas dos subárvores esquerda e direita).
    A classe AVLTree é essencial para a construção de uma árvore AVL, onde cada nó pode ter até dois filhos,
    e a organização dos nós permite operações eficientes de busca e manipulação, mantendo a árvore balanceada.
    A classe NodeAVL é usada internamente pela classe AVLTree para representar cada nó da árvore.
    A classe AVLTree é responsável por gerenciar a estrutura da árvore AVL, permitindo a inserção,
    busca e remoção de nós, além de percorrer a árvore em ordem.
    

    """
    def __init__(self):
        self.raiz = None

    def inserir(self, chave, objeto):
        self.raiz = self._inserir(self.raiz, chave, objeto)

    def _inserir(self, no, chave, objeto):
        if no is None:
            return NodeAVL(chave, objeto)
        if chave < no.chave:
            no.esquerda = self._inserir(no.esquerda, chave, objeto)
        elif chave > no.chave:
            no.direita = self._inserir(no.direita, chave, objeto)
        else:
            return no  # chaves duplicadas não são inseridas

        no.altura = 1 + max(self._altura(no.esquerda), self._altura(no.direita))
        balanceamento = self._get_balanceamento(no)

        # Rotação simples à direita
        if balanceamento > 1 and chave < no.esquerda.chave:
            return self._rotacionar_direita(no)

        # Rotação simples à esquerda
        if balanceamento < -1 and chave > no.direita.chave:
            return self._rotacionar_esquerda(no)

        # Rotação dupla esquerda-direita
        if balanceamento > 1 and chave > no.esquerda.chave:
            no.esquerda = self._rotacionar_esquerda(no.esquerda)
            return self._rotacionar_direita(no)

        # Rotação dupla direita-esquerda
        if balanceamento < -1 and chave < no.direita.chave:
            no.direita = self._rotacionar_direita(no.direita)
            return self._rotacionar_esquerda(no)

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

    def percurso_em_ordem(self):
        resultado = []
        self._em_ordem(self.raiz, resultado)
        return resultado

    def _em_ordem(self, no, resultado):
        if no:
            self._em_ordem(no.esquerda, resultado)
            resultado.append(no.objeto)
            self._em_ordem(no.direita, resultado) 

    def _altura(self, no):
        return no.altura if no else 0

    def _get_balanceamento(self, no):
        return self._altura(no.esquerda) - self._altura(no.direita) if no else 0

    def _rotacionar_direita(self, z):
        y = z.esquerda
        T3 = y.direita
        y.direita = z
        z.esquerda = T3
        z.altura = 1 + max(self._altura(z.esquerda), self._altura(z.direita))
        y.altura = 1 + max(self._altura(y.esquerda), self._altura(y.direita))
        return y

    def _rotacionar_esquerda(self, z):
        y = z.direita
        T2 = y.esquerda
        y.esquerda = z
        z.direita = T2
        z.altura = 1 + max(self._altura(z.esquerda), self._altura(z.direita))
        y.altura = 1 + max(self._altura(y.esquerda), self._altura(y.direita))
        return y
