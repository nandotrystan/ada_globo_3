from entidades.interacao import Interacao


class Conteudo:
    """
    Classe base para representar conteúdos como vídeos, podcasts e artigos.
    Atributos:
        - id_conteudo (int): Identificador único do conteúdo.
        - nome_conteudo (str): Nome do conteúdo.
        - interacoes (list): Lista de interações associadas ao conteúdo.
    Métodos:
        - __init__: Inicializa o conteúdo com um ID e nome.
        - id_conteudo: Retorna o ID do conteúdo.
        - nome_conteudo: Retorna o nome do conteúdo.
        - adicionar_interacao: Adiciona uma interação ao conteúdo.
        - calcular_total_interacoes_engajamento: Calcula o total de interações de engajamento (like, share, comment, view_start).
        - calcular_contagem_por_tipo_interacao: Calcula a contagem de interações por tipo.
        - calcular_tempo_total_consumo: Calcula o tempo total de consumo do conteúdo.
        - calcular_media_tempo_consumo: Calcula a média do tempo de consumo do conteúdo.
        - listar_comentarios: Lista os comentários associados ao conteúdo.
        - __str__: Retorna uma representação em string do conteúdo.
        - __repr__: Retorna uma representação detalhada do conteúdo.

    """
    def __init__(self, id_conteudo, nome_conteudo):
        self._id_conteudo = id_conteudo
        self._nome_conteudo = nome_conteudo
        self._interacoes = []

    @property
    def id_conteudo(self):
        return self._id_conteudo

    @property
    def nome_conteudo(self):
        return self._nome_conteudo
    
    @property
    def interacoes(self):
        return self._interacoes
    
    def adicionar_interacao(self, interacao):
        self._interacoes.append(interacao)

    def calcular_total_interacoes_engajamento(self):
        total = 0
        for interacao in self._interacoes:
            if interacao.tipo_interacao in ['like', 'share', 'comment', 'view_start']:
                # if interacao.tipo_interacao == 'comment' and interacao.comment_text:
                #     print(f"Comentário: {interacao.comment_text}")
                total += 1
        return total
    # # Calcula o total de interações de engajamento (like, share, comment).
    def calcular_contagem_por_tipo_interacao(self):
        contagem = {}
        for interacao in self._interacoes:
            if interacao.tipo_interacao not in contagem:
                contagem[interacao.tipo_interacao] = 0
            contagem[interacao.tipo_interacao] += 1
        return contagem

    def calcular_tempo_total_consumo(self):
        total_tempo = sum(interacao.watch_duration_seconds for interacao in self._interacoes)
        return total_tempo

    def calcular_media_tempo_consumo(self):
        tempos = [interacao.watch_duration_seconds for interacao in self._interacoes if interacao.watch_duration_seconds > 0]
        if not tempos:
            return 0
        return sum(tempos) / len(tempos)

    def listar_comentarios(self):
        comentarios = [interacao.comment_text for interacao in self._interacoes if interacao.comment_text]
        return comentarios
    
    def __str__(self):
        return f"{self.nome_conteudo} (ID: {self.id_conteudo})"

    def __repr__(self):
        return f"Conteudo(id_conteudo={self.id_conteudo}, nome_conteudo='{self.nome_conteudo}')"


class Video(Conteudo):
    """
    Classe que representa um vídeo.
    Atributos:
        - id_conteudo (int): Identificador único do vídeo.
        - nome_conteudo (str): Nome do vídeo.
        - duracao_total_video_seg (int): Duração total do vídeo em segundos.
    Métodos:
        - __init__: Inicializa o vídeo com um ID, nome e duração total.
        - duracao_total_video_seg: Retorna a duração total do vídeo em segundos.
        - calcular_percentual_medio_assistido: Calcula o percentual médio assistido do vídeo com base no tempo de consumo médio.

    """
    def __init__(self, id_conteudo, nome_conteudo, duracao_total_video_seg):
        super().__init__(id_conteudo, nome_conteudo)
        self.__duracao_total_video_seg = duracao_total_video_seg

    @property
    def duracao_total_video_seg(self):
        return self.__duracao_total_video_seg
    
    def adicionar_interacao(self, interacao):
        if not isinstance(interacao, Interacao):
            raise ValueError("Interação deve ser uma instância da classe Interacao.")
        super().adicionar_interacao(interacao)

    def calcular_percentual_medio_assistido(self):
        media_tempo_consumo = self.calcular_media_tempo_consumo()
        if self.__duracao_total_video_seg == 0:
            return 0
        return (media_tempo_consumo / self.__duracao_total_video_seg) * 100
    
    def calcular_tempo_total_consumo(self):
        total_tempo = super().calcular_tempo_total_consumo()
        return total_tempo if total_tempo <= self.__duracao_total_video_seg else self.__duracao_total_video_seg
    
    def calcular_media_tempo_consumo(self):
        tempos = [interacao.watch_duration_seconds for interacao in self._interacoes if interacao.watch_duration_seconds > 0]
        if not tempos:
            return 0
        media = sum(tempos) / len(tempos)
        return min(media, self.__duracao_total_video_seg)
    
    def listar_comentarios(self):
        return super().listar_comentarios()
    
    
    def __str__(self):
        return f"{self.nome_conteudo} (ID: {self.id_conteudo}, Duração: {self.duracao_total_video_seg} seg)"
    
    def __repr__(self):
        return f"Video(id_conteudo={self.id_conteudo}, nome_conteudo='{self.nome_conteudo}', duracao_total_video_seg={self.duracao_total_video_seg})"


class Podcast(Conteudo):
    """
    Classe que representa um podcast.
    Atributos:
        - id_conteudo (int): Identificador único do podcast.
        - nome_conteudo (str): Nome do podcast.
        - duracao_total_episodio_seg (int): Duração total do episódio em segundos.
    """
    def __init__(self, id_conteudo, nome_conteudo, duracao_total_episodio_seg=None):
        super().__init__(id_conteudo, nome_conteudo)
        self.__duracao_total_episodio_seg = duracao_total_episodio_seg

    @property
    def duracao_total_episodio_seg(self):
        return self.__duracao_total_episodio_seg
    
    def adicionar_interacao(self, interacao):
        if not isinstance(interacao, Interacao):
            raise ValueError("Interação deve ser uma instância da classe Interacao.")
        super().adicionar_interacao(interacao)
    
    
    def calcular_tempo_total_consumo(self):
        if self.__duracao_total_episodio_seg is None:
            return super().calcular_tempo_total_consumo()
        total_tempo = super().calcular_tempo_total_consumo()
        return total_tempo if total_tempo <= self.__duracao_total_episodio_seg else self.__duracao_total_episodio_seg
    
    def calcular_media_tempo_consumo(self):
        if self.__duracao_total_episodio_seg is None:
            return super().calcular_media_tempo_consumo()
        tempos = [interacao.watch_duration_seconds for interacao in self._interacoes if interacao.watch_duration_seconds > 0]
        if not tempos:
            return 0
        media = sum(tempos) / len(tempos)
        return min(media, self.__duracao_total_episodio_seg) if self.__duracao_total_episodio_seg else media
    
    def listar_comentarios(self):
        return super().listar_comentarios()
    

    def __str__(self):
        return f"{self.nome_conteudo} (ID: {self.id_conteudo}, Duração Episódio: {self.duracao_total_episodio_seg} seg)" if self.__duracao_total_episodio_seg else f"{self.nome_conteudo} (ID: {self.id_conteudo})"
    def __repr__(self):
        return f"Podcast(id_conteudo={self.id_conteudo}, nome_conteudo='{self.nome_conteudo}', duracao_total_episodio_seg={self.duracao_total_episodio_seg})"

class Artigo(Conteudo):
    """
    Classe que representa um artigo.
    Atributos:
        - id_conteudo (int): Identificador único do artigo.
        - nome_conteudo (str): Nome do artigo.
        - tempo_leitura_estimado_seg (int): Tempo estimado de leitura do artigo em segundos.
    """

    def __init__(self, id_conteudo, nome_conteudo, tempo_leitura_estimado_seg):
        super().__init__(id_conteudo, nome_conteudo)
        self.__tempo_leitura_estimado_seg = tempo_leitura_estimado_seg
        self.__interacoes = []
    @property
    def tempo_leitura_estimado_seg(self):

        return self.__tempo_leitura_estimado_seg
    
    def adicionar_interacao(self, interacao):
        if not isinstance(interacao, Interacao):
            raise ValueError("Interação deve ser uma instância da classe Interacao.")
        super().adicionar_interacao(interacao)
        self.__interacoes.append(interacao)
    
    def calcular_tempo_total_consumo(self):
        if self.__tempo_leitura_estimado_seg is None:
            return super().calcular_tempo_total_consumo()
        total_tempo = super().calcular_tempo_total_consumo()
        return total_tempo if total_tempo <= self.__tempo_leitura_estimado_seg else self.__tempo_leitura_estimado_seg
    
    def calcular_media_tempo_consumo(self):
        if self.__tempo_leitura_estimado_seg is None:
            return super().calcular_media_tempo_consumo()
        tempos = [interacao.watch_duration_seconds for interacao in self._interacoes if interacao.watch_duration_seconds > 0]
        if not tempos:
            return 0
        media = sum(tempos) / len(tempos)
        return min(media, self.__tempo_leitura_estimado_seg) if self.__tempo_leitura_estimado_seg else media
    
    def listar_comentarios(self):
        if not self.__interacoes:
            return []
        return super().listar_comentarios()
    
    def __str__(self):
        return f"{self.nome_conteudo} (ID: {self.id_conteudo}, Tempo de Leitura Estimado: {self.tempo_leitura_estimado_seg} seg)" if self.tempo_leitura_estimado_seg else f"{self.nome_conteudo} (ID: {self.id_conteudo})"
    def __repr__(self):
        return f"Artigo(id_conteudo={self.id_conteudo}, nome_conteudo='{self.nome_conteudo}', tempo_leitura_estimado_seg={self.tempo_leitura_estimado_seg})"
