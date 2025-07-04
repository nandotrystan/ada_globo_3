class Plataforma:
    """
    Classe que representa uma plataforma de conteúdo digital.
    Atributos:
        - id_plataforma (int): Identificador único da plataforma.
        - nome_plataforma (str): Nome da plataforma.
    Métodos:
        - __init__: Inicializa a plataforma com um nome e um ID opcional.
        - id_plataforma: Retorna o ID da plataforma.
        - nome_plataforma: Retorna o nome da plataforma.
        - nome_plataforma.setter: Permite atualizar o nome da plataforma.
        - __str__: Retorna uma representação em string do nome da plataforma.
        - __repr__: Retorna uma representação detalhada da plataforma.
        - __eq__: Permite comparar duas plataformas com base no nome.
        - __hash__: Permite usar a plataforma como chave em dicionários ou conjuntos.
    """
    def __init__(self, nome_plataforma, id_plataforma=None):
        if not nome_plataforma:
            raise ValueError("O nome da plataforma não pode ser vazio.")
        self.__id_plataforma = id_plataforma
        self.__nome_plataforma = nome_plataforma

    @property
    def id_plataforma(self):
        return self.__id_plataforma

    @property
    def nome_plataforma(self):
        return self.__nome_plataforma

    @nome_plataforma.setter
    def nome_plataforma(self, novo_nome):
        if not novo_nome:
            raise ValueError("O nome da plataforma não pode ser vazio.")
        self.__nome_plataforma = novo_nome

    def __str__(self):
        return self.nome_plataforma
    
    # Representa a plataforma como uma string simples, retornando apenas o nome.
    def __repr__(self):
        return f"Plataforma(nome='{self.nome_plataforma}')"
    
    def __eq__(self, other):
        if isinstance(other, Plataforma):
            return self.nome_plataforma == other.nome_plataforma
        return False
    # # Permite comparar duas plataformas com base no nome.
    def __hash__(self):
        return hash(self.nome_plataforma)