from datetime import datetime

class Interacao:
    """
    Classe que representa uma interação do usuário com um conteúdo em uma plataforma específica.
    Atributos:
        - id_usuario (int): Identificador único do usuário que realizou a interação.
        - conteudo_associado (Conteudo): Conteúdo associado à interação.
        - plataforma_interacao (Plataforma): Plataforma onde a interação ocorreu.
        - tipo_interacao (str): Tipo de interação realizada (view_start, like, share, comment).
        - watch_duration_seconds (int): Duração da visualização em segundos, se aplicável.
        - comment_text (str): Texto do comentário, se aplicável.
        - timestamp_interacao (datetime): Data e hora da interação.
    Métodos:
        - __init__: Inicializa a interação com os dados brutos, conteúdo associado e plataforma de interação.
        - Propriedades para acessar os atributos privados.
        - __str__: Retorna uma representação em string da interação.
        - __repr__: Retorna uma representação detalhada da interação.
    """
    
    TIPOS_INTERACAO_VALIDOS = {'view_start', 'like', 'share', 'comment'}

    def __init__(self, dados_brutos, conteudo_associado, plataforma_interacao):
        self.__conteudo_associado = conteudo_associado
        self.__plataforma_interacao = plataforma_interacao

        self.__id_usuario = int(dados_brutos['id_usuario'])
        self.__timestamp_interacao = datetime.fromisoformat(dados_brutos['timestamp_interacao'])
        
        tipo_interacao = dados_brutos['tipo_interacao']
        if tipo_interacao not in Interacao.TIPOS_INTERACAO_VALIDOS:
            raise ValueError(f"Tipo de interação inválido: {tipo_interacao}")
        self.__tipo_interacao = tipo_interacao

        self.__watch_duration_seconds = int(dados_brutos.get('watch_duration_seconds', 0))
        if self.__watch_duration_seconds < 0:
            raise ValueError("Watch duration cannot be negative.")

        self.__comment_text = dados_brutos.get('comment_text', '').strip()
    @property
    def interacao_id(self):
        return self.__interacao_id
    @property
    def conteudo_associado(self):
        return self.__conteudo_associado
    @property
    def id_usuario(self):
        return self.__id_usuario
    @property
    def timestamp_interacao(self):
        return self.__timestamp_interacao
    @property
    def plataforma_interacao(self):
        return self.__plataforma_interacao
    @property
    def tipo_interacao(self):
        return self.__tipo_interacao
    @property
    def watch_duration_seconds(self):
        return self.__watch_duration_seconds
    @property
    def comment_text(self):
        return self.__comment_text
    
    def __str__(self):
        return f"Interacao(id_usuario={self.id_usuario}, conteudo={self.conteudo_associado.nome_conteudo}, tipo={self.tipo_interacao}, plataforma={self.plataforma_interacao.nome_plataforma})"
    def __repr__(self): 
        return f"Interacao(id_usuario={self.id_usuario}, conteudo_associado={self.conteudo_associado}, plataforma_interacao={self.plataforma_interacao}, tipo_interacao='{self.tipo_interacao}', watch_duration_seconds={self.watch_duration_seconds}, comment_text='{self.comment_text}')"
