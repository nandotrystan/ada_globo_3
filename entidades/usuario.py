from entidades.interacao import Interacao
from entidades.plataforma import Plataforma

class Usuario:
    """
    Classe que representa um usuário do sistema de análise de engajamento.
    Atributos:
        - id_usuario (int): Identificador único do usuário.
        - interacoes_realizadas (list): Lista de interações realizadas pelo usuário.
    Métodos:
        - __init__: Inicializa o usuário com um ID e uma lista de interações.
        - registrar_interacao: Registra uma interação do usuário, garantindo que seja uma instância da classe Interacao.
        - obter_interacoes_por_tipo: Retorna as interações do usuário filtradas por tipo.
        - obter_conteudos_unicos_consumidos: Retorna os conteúdos únicos consumidos pelo usuário.
        - calcular_tempo_total_consumo_plataforma: Calcula o tempo total de consumo em uma plataforma específica.
        - plataformas_mais_frequentes: Retorna as plataformas mais frequentes usadas pelo usuário.
    """
    def __init__(self, id_usuario):
        self.__id_usuario = id_usuario
        self.__interacoes_realizadas = []

    @property
    def id_usuario(self):
        return self.__id_usuario

    # def registrar_interacao(self, interacao):
    #     if not isinstance(interacao, Interacao):
    #         raise ValueError("Interação deve ser uma instância da classe Interacao.")
    #     self.__interacoes_realizadas.append(interacao)

    def registrar_interacao(self, interacao):
        if not isinstance(interacao, Interacao):
            raise ValueError(f"Interação deve ser uma instância da classe Interacao, mas foi passado um objeto do tipo {type(interacao).__name__}")
        if interacao not in self.__interacoes_realizadas:
            self.__interacoes_realizadas.append(interacao)
            return interacao

    def obter_interacoes_por_tipo(self, tipo_desejado):
        if tipo_desejado not in Interacao.TIPOS_INTERACAO_VALIDOS:
            raise ValueError(f"Tipo de interação inválido: {tipo_desejado}")
        for i in self.__interacoes_realizadas:
            if not isinstance(i, Interacao):
                raise TypeError(f"Interação inválida: {i}. Esperado uma instância da classe Interacao.")
            if i.tipo_interacao == tipo_desejado:
                print(f"Conteúdo: {i.conteudo_associado.nome_conteudo}, Interação: {i.tipo_interacao}, Plataforma: {i.plataforma_interacao.nome_plataforma}, Duração: {i.watch_duration_seconds} segundos, Timestamp: {i.timestamp_interacao}")

        return [i for i in self.__interacoes_realizadas if i.tipo_interacao == tipo_desejado]

    def obter_conteudos_unicos_consumidos(self):
        return {i.conteudo_associado for i in self.__interacoes_realizadas}

    def calcular_tempo_total_consumo_plataforma(self, plataforma):
        if not isinstance(plataforma, Plataforma):
            raise ValueError("Plataforma deve ser uma instância da classe Plataforma.")
        return sum(i.watch_duration_seconds for i in self.__interacoes_realizadas if i.plataforma_interacao == plataforma)

    def plataformas_mais_frequentes(self, top_n=3):
        contagem = {}
        for interacao in self.__interacoes_realizadas:
            plataforma = interacao.plataforma_interacao.nome_plataforma
            if plataforma not in contagem:
                contagem[plataforma] = 0
            contagem[plataforma] += 1
        sorted_plataformas = sorted(contagem.items(), key=lambda x: x[1], reverse=True)
        return [plataforma for plataforma, _ in sorted_plataformas[:top_n]]

    def calcular_tempo_total_consumo(self):
        """
        Calcula o tempo total de consumo em todas as interações do usuário.
        :return: Tempo total de consumo em segundos.
        """
        return sum(i.watch_duration_seconds for i in self.__interacoes_realizadas)
    
    def calcular_total_interacoes(self):
        """
        Calcula o total de interações realizadas pelo usuário.
        :return: Número total de interações.
        """
        return len(self.__interacoes_realizadas)

    def __str__(self):
        return f"Usuario(ID: {self.id_usuario})"

    def __repr__(self):
        return f"Usuario(id_usuario={self.id_usuario})"