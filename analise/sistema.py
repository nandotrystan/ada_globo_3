import csv
from collections import defaultdict
from entidades.plataforma import Plataforma
from estrutura_dados.fila import FilaCSV
from estrutura_dados.arvore_binaria_busca import AVLTree as BST
from entidades.conteudo import Conteudo
from entidades.usuario import Usuario
from entidades.interacao import Interacao
from ordenação.ordenacao import quick_sort, insertion_sort, merge_sort
 # ou merge_sort, ou bubble_sort, ou selection_sort, ou counting_sort, ou bucket_sort, ou shell_sort, ou cocktail_sort, ou gnome_sort

  # ou insertion_sort

class SistemaAnaliseEngajamento:
    def __init__(self):
        self._fila_interacoes_brutas = FilaCSV()
        self._arvore_conteudos = BST()
        self._arvore_usuarios = BST()
        self._plataformas_registradas = {}

    def _carregar_interacoes_csv(self, caminho_arquivo: str):
        with open(caminho_arquivo, newline='', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor)  # Pula cabeçalho
            for linha in leitor:
                self._fila_interacoes_brutas.enfileirar(linha)

    def _ordenar(self, lista, metrica=None, key_func=None, algoritmo='auto'):
        """
        Ordena uma lista de objetos usando o algoritmo escolhido (quick, insertion, merge ou auto).

        Parâmetros:
        - lista: lista de objetos a serem ordenados.
        - metrica: nome do atributo ou método a ser usado para ordenação (string).
        - key_func: função opcional que retorna o valor a ser usado na ordenação.
        - algoritmo: 'quick', 'insertion', 'merge' ou 'auto' (seleciona com base no tamanho da lista).
        """
        if not lista:
            return []

        # Decide a função de chave com prioridade para key_func
        chave_funcional = key_func
        if not key_func and metrica:
            chave_funcional = lambda obj: getattr(obj, metrica)() if callable(getattr(obj, metrica)) else getattr(obj, metrica)

        # Seleciona o algoritmo com base no tipo ou tamanho
        if algoritmo == 'auto':
            algoritmo = 'insertion' if len(lista) <= 20 else 'quick'

        if algoritmo == 'quick':
            return quick_sort(lista, key_func=chave_funcional)
        elif algoritmo == 'insertion':
            return insertion_sort(lista, key_func=chave_funcional)
        elif algoritmo == 'merge':
            return merge_sort(lista, key_func=chave_funcional)
        else:
            raise ValueError(f"Algoritmo de ordenação desconhecido: {algoritmo}")

    def processar_interacoes_da_fila(self):
        """
        Processa as interações da fila, registrando conteúdos, usuários e interações.
        Essa função faz o processamento linha a linha de uma fila de interações, 
        preenchendo árvores binárias de busca (_arvore_conteudos, _arvore_usuarios), 
        mapeando plataformas e criando objetos de Interacao, Conteudo e Usuario.

        ⏱️ Análise de Complexidade
        1. Desenfileirar cada linha da fila:
        Tempo: O(n) — onde n é o número de interações na fila.
        Espaço: O(1) — apenas variáveis temporárias para cada linha.
        2. Processar cada linha:
        - Conversão de tipos (int, str) e manipulação de strings:
        Tempo: O(1) — operações constantes para cada linha.
        Espaço: O(1) — apenas variáveis temporárias.
        - Verificação e inserção na árvore de conteúdos:
        Tempo: O(log m) — onde m é o número de conteúdos já registrados (média).
        Espaço: O(1) — apenas variáveis temporárias.
        - Verificação e inserção na árvore de usuários:
        Tempo: O(log k) — onde k é o número de usuários já registrados (média).
        Espaço: O(1) — apenas variáveis temporárias.
        - Criação de objetos Interacao, Conteudo e Usuario:
        Tempo: O(1) — operações constantes para cada linha.
        Espaço: O(1) — apenas variáveis temporárias.
        3. Adicionar interações ao conteúdo e registrar no usuário:
        Tempo: O(1) — operações constantes para cada linha.
        Espaço: O(1) — apenas variáveis temporárias.
        4. Total:
        Tempo: O(n * (log m + log k)) — onde n é o número
        de interações, m é o número de conteúdos e k é o número de usuários.
        Espaço: O(1) — apenas variáveis temporárias.

        """
        while not self._fila_interacoes_brutas.esta_vazia():
            linha = self._fila_interacoes_brutas.desenfileirar()
            try:
                id_conteudo = int(linha[0].strip())
                nome_conteudo = linha[1].strip().capitalize()
                id_usuario = int(linha[2].strip())
                timestamp_interacao = linha[3].strip()
                nome_plataforma = linha[4].strip()
                tipo_interacao = linha[5].strip()
                try:
                    tempo_consumo = int(linha[6].strip())
                except ValueError:
                    tempo_consumo = 0
                comentario = linha[7].strip() if len(linha) > 7 else ""

                # Plataforma
                if nome_plataforma not in self._plataformas_registradas:
                    self._plataformas_registradas[nome_plataforma] = Plataforma(nome_plataforma)
                plataforma = self._plataformas_registradas[nome_plataforma]

                # Conteúdo
                conteudo = self._arvore_conteudos.buscar(id_conteudo)
                if not conteudo:
                    conteudo = Conteudo(id_conteudo, nome_conteudo)
                    self._arvore_conteudos.inserir(id_conteudo, conteudo)
                else:
                    # opcional: atualizar nome se desejar
                    if not conteudo.nome_conteudo or conteudo.nome_conteudo.startswith("Conteudo_"):
                        conteudo.nome_conteudo = nome_conteudo

                # Usuário
                usuario = self._arvore_usuarios.buscar(id_usuario)
                if not usuario:
                    usuario = Usuario(id_usuario)
                    self._arvore_usuarios.inserir(id_usuario, usuario)

              

                dados_brutos = {
                    'id_usuario': id_usuario,
                    'timestamp_interacao': timestamp_interacao,
                    'tipo_interacao': tipo_interacao,
                    'watch_duration_seconds': tempo_consumo,
                    'comment_text': comentario
                }
                interacao = Interacao(dados_brutos, conteudo, plataforma)


                conteudo.adicionar_interacao(interacao)
                print(f"[OK] Interação registrada - Conteúdo: {conteudo.nome_conteudo}, Usuário: {id_usuario}, Tipo: {tipo_interacao}, Duração: {tempo_consumo}")
                usuario.registrar_interacao(interacao)

            except Exception as e:
                print(f"[ERRO] Linha inválida: {linha} - Motivo: {e}")
        print(f"\nTotal de conteúdos: {len(self._arvore_conteudos.percurso_em_ordem())}")
        print(f"Total de usuários: {len(self._arvore_usuarios.percurso_em_ordem())}")
        
        
        

    def gerar_relatorio_engajamento_conteudos(self, top_n: int = None):
        """
        Gera um relatório de engajamento dos conteúdos, ordenando-os por diferentes métricas
        como total de interações, tempo total de consumo e engajamento médio.
        
        Chama identificar_top_conteudos para ordenar os conteúdos com base na quantidade de interações de engajamento.

        Imprime os top_n conteúdos com:
        ID
        Nome
        Total de interações de engajamento
        Tempo total de consumo

        ⏱️ Análise de Complexidade
        1. percurso_em_ordem() da árvore de conteúdos:
        Tempo: O(n) — onde n é o número de conteúdos na árvore.
        Espaço: O(n) — para armazenar a lista de conteúdos.
        2. identificar_top_conteudos("calcular_total_interacoes_engajamento", top_n):
        Tempo: O(n log n) — onde n é o número de conteúdos.
        Espaço: O(n) — para armazenar a lista de conteúdos ordenados.
        3. Loop de impressão dos top_n conteúdos:
        Tempo: O(top_n) — geralmente pequeno e constante (ex: 5 ou 10).
        Espaço: O(1) — apenas variáveis temporárias.
        4. Total:
        Tempo: O(n + n log n + top_n) — onde n é o número de conteúdos.
        Espaço: O(n) — para armazenar a lista de conteúdos ordenados.
        5. Observação:
        Se top_n for None, a função retorna todos os conteúdos ordenados.

        """
        ordenados = self.identificar_top_conteudos("calcular_total_interacoes_engajamento", top_n)
        return ordenados
        # print("\n📈 Top Conteúdos por Interações:")
        # for conteudo in ordenados:
        #     print(f"{conteudo.id_conteudo} - {conteudo.nome_conteudo} | Interações: {conteudo.calcular_total_interacoes_engajamento()} | Tempo Total de Consumo: {conteudo.calcular_tempo_total_consumo()} segundos")
        
    def gerar_relatorio_atividade_usuarios(self, top_n: int = None):
        """
        Gera um relatório de atividade dos usuários, ordenando-os por total de interações.
        Imprime os top_n usuários com:
        ID do usuário
        Total de interações
        ⏱️ Análise de Complexidade
        1. percurso_em_ordem() da árvore de usuários:
        Tempo: O(n) — onde n é o número de usuários na árvore.
        Espaço: O(n) — para armazenar a lista de usuários.
        2. quick_sort(usuarios, "calcular_total_interacoes"):
        Tempo médio: O(n log n) — onde n é o número de usuários.
        Tempo pior caso: O(n²) — se o pivô estiver sempre mal escolhido.
        Espaço: O(log n) — para a pilha de recursão do quick_sort.
        3. Loop de impressão dos top_n usuários:
        Tempo: O(top_n) — geralmente pequeno e constante (ex: 5 ou 10).
        Espaço: O(1) — apenas variáveis temporárias.
        4. Total:
        Tempo: O(n + n log n + top_n) — onde n é o número de usuários.
        Espaço: O(n) — para armazenar a lista de usuários.

        """
        usuarios = self._arvore_usuarios.percurso_em_ordem()

        if not usuarios:
            print("Nenhum usuário registrado.")
            return

        # Ordena os usuários pelo total de interações (decrescente)
        # ordenados = self._ordenar(lista=usuarios, metrica="calcular_total_interacoes", algoritmo="auto")
        
        ordenados = merge_sort(usuarios, "calcular_total_interacoes")

        if top_n is not None:
            ordenados = ordenados[:top_n]

        print(f"Top {top_n if top_n else len(ordenados)} Usuários por Total de Interações:")
        for i, usuario in enumerate(ordenados, 1):
            print(f"{i}. Usuário ID: {usuario.id_usuario} - Total de Interações: {usuario.calcular_total_interacoes()}")
    
    def identificar_top_conteudos(self, metrica: str, n: int = None):
        """
        Identifica os top conteúdos com base em uma métrica específica.
        Parâmetros:
        - metrica: string com o nome do método a ser usado para ordenação (ex   : "calcular_tempo_total_consumo").
        - n: número de conteúdos a serem retornados (se None, retorna todos).
        Retorna:
        - Lista dos conteúdos ordenados pela métrica especificada.
        ⏱️ Análise de Complexidade
        1. percurso_em_ordem() da árvore de conteúdos:
        Tempo: O(n) — onde n é o número de conteúdos na árvore.
        Espaço: O(n) — para armazenar a lista de conteúdos.
        2. insertion_sort(conteudos, metrica):
        Tempo médio: O(n log n) — onde n é o número de conteúdos.
        Tempo pior caso: O(n²) — se a lista já estiver ordenada ou quase ordenada.
        Espaço: O(n) — para armazenar a lista ordenada.
        3. Loop de impressão dos top_n conteúdos:
        Tempo: O(n) — onde n é o número de conteúdos a serem impressos.
        Espaço: O(1) — apenas variáveis temporárias.
        4. Total:
        Tempo: O(n + n log n + n) — onde n é o número de conteúdos.
        Espaço: O(n) — para armazenar a lista de conteúdos ordenados.
        5. Observação:
        Se n for None, a função retorna todos os conteúdos ordenados.
        Se n for um valor positivo, retorna apenas os top_n conteúdos ordenados.

        """
        conteudos = self._arvore_conteudos.percurso_em_ordem()
        ordenados = insertion_sort(conteudos, metrica)
        if not ordenados:
            print("Nenhum conteúdo registrado.")
            return []
        print(f"Top {n if n else len(ordenados)} Conteúdos por {metrica.replace('_', ' ').title()}:")
        for i, conteudo in enumerate(ordenados[:n], 1):
            print(f"{i}. Conteúdo ID: {conteudo.id_conteudo} - Nome: {conteudo.nome_conteudo} - {metrica.replace('_', ' ').title()}: {getattr(conteudo, metrica)()}")
        return ordenados[:n] if n else ordenados

    def identificar_top_plataformas(self, tipo_engajamento=None, top_n=5):
        """
        Identifica as plataformas com maior número de interações de engajamento.
        Parâmetros:
        - tipo_engajamento: string com o tipo de interação a ser filtrado (ex: "share", "like", "comment", "view_start").
        - top_n: número de plataformas a serem retornadas (se None, retorna todas).
        Retorna:
        - Lista das plataformas ordenadas pelo total de interações.
        ⏱️ Análise de Complexidade
        1. percurso_em_ordem() da árvore de conteúdos:
        Tempo: O(n) — onde n é o número de conteúdos na árvore.
        Espaço: O(n) — para armazenar a lista de conteúdos.
        2. Loop para contar interações por plataforma:
        Tempo: O(n * m) — onde n é o número de conteúdos e m é o número de interações por conteúdo.
        Espaço: O(p) — onde p é o número de plataformas distintas.
        3. insertion_sort(plataformas_total.items(), key_func):
        Tempo médio: O(p log p) — onde p é o número de plataformas distintas.
        Tempo pior caso: O(p²) — se a lista já estiver ordenada ou quase ordenada.
        Espaço: O(log p) — para a pilha de recursão do insertion_sort.
        4. Loop de impressão dos top_n plataformas:
        Tempo: O(top_n) — geralmente pequeno e constante (ex: 5 ou  10).
        Espaço: O(1) — apenas variáveis temporárias.
        5. Total:
        Tempo: O(n + n * m + p log p + top_n) — onde n é o número de conteúdos, m é o número de interações por conteúdo e p é o número de plataformas distintas.
        Espaço: O(n + p) — para armazenar as interações e plataformas.

        """
        plataformas_total = defaultdict(int)
        plataformas_por_tipo = defaultdict(lambda: defaultdict(int))

        for conteudo in self._arvore_conteudos.percurso_em_ordem():
            for interacao in conteudo.interacoes:
                tipo = interacao.tipo_interacao.strip().lower()
                nome_plataforma = interacao.plataforma_interacao.nome_plataforma

                # Filtra se necessário
                if tipo_engajamento is None or tipo == tipo_engajamento:
                    plataformas_total[nome_plataforma] += 1
                    plataformas_por_tipo[nome_plataforma][tipo] += 1

        # Ordenar as plataformas por total
        plataformas_ordenadas = insertion_sort(list(plataformas_total.items()), key_func=lambda x: x[1])

        # Título
        tipo_txt = f"do tipo '{tipo_engajamento}'" if tipo_engajamento else "de todos os tipos"
        print(f"\nTop {top_n} plataformas por interações {tipo_txt}:")

        for i, (nome, total) in enumerate(plataformas_ordenadas[:top_n], 1):
            print(f"{i}. {nome} - {total} interações")
            if tipo_engajamento is None:
                for tipo in ["share", "like", "comment", "view_start"]:
                    qtd = plataformas_por_tipo[nome][tipo]
                    print(f"   - {tipo.capitalize()}: {qtd} interações")
            else:
                qtd = plataformas_por_tipo[nome][tipo_engajamento]
                print(f"   - {tipo_engajamento.capitalize()}: {qtd} interações")

        return plataformas_ordenadas[:top_n] if top_n else plataformas_ordenadas
    
    
    def identificar_top_usuarios_tempo_consumo(self, top_n=10):
        """
        Identifica os usuários com maior tempo total de consumo de conteúdo.
        Parâmetros:
        - top_n: número de usuários a serem retornados (se None, retorna todos).
        Retorna:
        - Lista dos usuários ordenados pelo tempo total de consumo.
        ⏱️ Análise de Complexidade
        1. percurso_em_ordem() da árvore de usuários:
        Tempo: O(n) — onde n é o número de usuários na árvore.
        Espaço: O(n) — para armazenar a lista de usuários.
        2. merge_sort(usuarios, "calcular_tempo_total_consumo"):
        Tempo médio: O(n log n) — onde n é o número de usuários.
        Tempo pior caso: O(n²) — se o pivô estiver sempre mal escolhido.
        Espaço: O(log n) — para a pilha de recursão do merge_sort.
        3. Loop de impressão dos top_n usuários:
        Tempo: O(top_n) — geralmente pequeno e constante (ex: 5 ou 10).
        Espaço: O(1) — apenas variáveis temporárias.
        4. Total:
        Tempo: O(n + n log n + top_n) — onde n é o número de usuários.
        Espaço: O(n) — para armazenar a lista de usuários.
        5. Observação:
        Se top_n for None, a função retorna todos os usuários ordenados.

        """
        usuarios = self._arvore_usuarios.percurso_em_ordem()
        
        # Ordena com base no método calcular_tempo_total_consumo
        usuarios_ordenados = merge_sort(usuarios, "calcular_tempo_total_consumo")
        
        print(f"Top {top_n} usuários por tempo total de consumo:")
        for i, u in enumerate(usuarios_ordenados[:top_n], 1):
            total = u.calcular_tempo_total_consumo()
            print(f"{i}. Usuário {u.id_usuario} - {total} segundos")
    
    def identificar_top_usuarios(self, metrica: str, n: int = None):
        """
        Identifica os top usuários com base em uma métrica específica.
        Parâmetros:
        - metrica: string com o nome do método a ser usado para ordenação (ex: "calcular_tempo_total_consumo").
        - n: número de usuários a serem retornados (se None, retorna todos).
        Retorna:
        - Lista dos usuários ordenados pela métrica especificada.
        ⏱️ Análise de Complexidade
        1. percurso_em_ordem() da árvore de usuários:
        Tempo: O(n) — onde n é o número de usuários na árvore.
        Espaço: O(n) — para armazenar a lista de usuários.
        2. merge_sort(usuarios, metrica):
        Tempo médio: O(n log n) — onde n é o número de usuários.
        Tempo pior caso: O(n²) — se o pivô estiver sempre mal escolhido.
        Espaço: O(log n) — para a pilha de recursão do merge_sort.
        3. Loop de impressão dos top_n usuários:
        Tempo: O(n) — onde n é o número de usuários a serem impressos.
        Espaço: O(1) — apenas variáveis temporárias.
        4. Total:
        Tempo: O(n + n log n + n) — onde n é o número de usuários.
        Espaço: O(n) — para armazenar a lista de usuários ordenados.

        """
        usuarios = self._arvore_usuarios.percurso_em_ordem()
        ordenados = merge_sort(usuarios, metrica)
        if not ordenados:
            print("Nenhum usuário registrado.")
            return []
        print(f"Top {n if n else len(ordenados)} Usuários por {metrica.replace('_', ' ').title()}:")
        for i, usuario in enumerate(ordenados[:n], 1):
            print(f"{i}. Usuário ID: {usuario.id_usuario} - {metrica.replace('_', ' ').title()}: {getattr(usuario, metrica)()}")
        return ordenados[:n] if n else ordenados
    
    def identificar_top_conteudos_comentados(self, top_n=5):
        """
        Identifica os conteúdos mais comentados e imprime os top_n conteúdos com mais comentários.
        Parâmetros:
        - top_n: número de conteúdos a serem retornados (se None, retorna todos).
        Retorna:
        - Lista dos conteúdos ordenados pela quantidade de comentários.
        ⏱️ Análise de Complexidade
        1. percurso_em_ordem() da árvore de conteúdos:
        Tempo: O(n) — onde n é o número de conteúdos na árvore.
        Espaço: O(n) — para armazenar a lista de conteúdos.
        2. Loop para contar comentários por conteúdo:
        Tempo: O(n * m) — onde n é o número de conteúdos e m é o número de interações por conteúdo.
        Espaço: O(m) — onde m é o número de conteúdos distintos.
        3. insertion_sort(lista, key_func):
        Tempo médio: O(m log m) — onde m é o número de conteúdos distintos.
        Tempo pior caso: O(m²) — se a lista já estiver ordenada ou quase ordenada.
        Espaço: O(log m) — para a pilha de recursão do insertion_sort.
        4. Loop de impressão dos top_n conteúdos:
        Tempo: O(top_n) — geralmente pequeno e constante (ex: 5 ou 10).
        Espaço: O(1) — apenas variáveis temporárias.

        """
        conteudos = self._arvore_conteudos.percurso_em_ordem()
        # Mapeia cada conteúdo para sua contagem de comentários
        lista = []
        for conteudo in conteudos:
            total_comentarios = sum(
                1 for i in conteudo.interacoes
                if i.tipo_interacao == "comment"
            )
            lista.append((conteudo, total_comentarios))

        # Ordena usando quick_sort se quiser (decrescente pelo total de comentários)
        lista_ordenada = insertion_sort(lista, key_func=lambda x: x[1])

        print(f"\nTop {top_n} conteúdos mais comentados:")
        for i, (conteudo, total) in enumerate(lista_ordenada[:top_n], 1):
            print(f"{i}. {conteudo.nome_conteudo} (ID {conteudo.id_conteudo}) - {total} comentários")
        
        return lista_ordenada[:top_n] if top_n else lista_ordenada
    
    # Total de interações por tipo de conteúdo (Liste os conteúdos com maior quantidade de interações).
    def identificar_total_interacoes_por_tipo_conteudo(self, top_n=100):
        """
        Identifica o total de interações por tipo de conteúdo e imprime os top_n conteúdos com mais interações.
        Parâmetros:
        - top_n: número de conteúdos a serem retornados (se None, retorna todos).   
        Retorna:
        - Lista dos conteúdos ordenados pelo total de interações.
        ⏱️ Análise de Complexidade
        1. percurso_em_ordem() da árvore de conteúdos:
        Tempo: O(n) — onde n é o número de conteúdos na árvore.
        Espaço: O(n) — para armazenar a lista de conteúdos.
        2. Loop para contar interações por conteúdo:
        Tempo: O(n * m) — onde n é o número de conteúdos e m é o número de interações por conteúdo.
        Espaço: O(m) — onde m é o número de conteúdos distintos.
        3. insertion_sort(conteudos, key_func):
        Tempo médio: O(m log m) — onde m é o número de conteúdos distintos.
        Tempo pior caso: O(m²) — se a lista já estiver ordenada ou quase ordenada.
        Espaço: O(log m) — para a pilha de recursão do insertion_sort.
        4. Loop de impressão dos top_n conteúdos:
        Tempo: O(top_n) — geralmente pequeno e constante (ex: 5 ou 10).
        Espaço: O(1) — apenas variáveis temporárias.
        5. Total:
        Tempo: O(n + n * m + m log m + top_n) — onde n é o número de conteúdos, m é o número de interações por conteúdo e m é o número de conteúdos distintos.
        Espaço: O(n + m) — para armazenar as interações e conteúdos.

        """
        conteudos = self._arvore_conteudos.percurso_em_ordem()
        total_interacoes = defaultdict(int)

        for conteudo in conteudos:
            total_interacoes[conteudo.nome_conteudo] += len(conteudo.interacoes)

        # Ordena os conteúdos pelo total de interações (decrescente)
        conteudos_ordenados = insertion_sort(list(total_interacoes.items()), key_func=lambda x: x[1])

        print(f"\nTop {top_n} conteúdos por total de interações:")
        for i, (nome, total) in enumerate(conteudos_ordenados[:top_n], 1):
            print(f"{i}. {nome} - {total} interações")
        
        return conteudos_ordenados[:top_n] if top_n else conteudos_ordenados
    
    def identificar_tempo_medio_consumo_por_plataforma(self, top_n=5):
        """
        Identifica o tempo médio de consumo por plataforma e imprime os top_n plataformas com maior média de consumo.
        Parâmetros:
        - top_n: número de plataformas a serem retornadas (se None, retorna todas).
        Retorna:
        - Lista das plataformas ordenadas pelo tempo médio de consumo.
        ⏱️ Análise de Complexidade
        1. percurso_em_ordem() da árvore de conteúdos:
        Tempo: O(n) — onde n é o número de conteúdos na árvore.
        Espaço: O(n) — para armazenar a lista de conteúdos.
        2. Loop para calcular o tempo médio de consumo por plataforma:
        Tempo: O(n * m) — onde n é o número de conteúdos e m é o número de interações por conteúdo.
        Espaço: O(p) — onde p é o número de plataformas distintas.
        3. insertion_sort(plataformas.items(), key_func):
        Tempo médio: O(p log p) — onde p é o número de plataformas distintas.
        Tempo pior caso: O(p²) — se a lista já estiver ordenada ou quase ordenada.
        Espaço: O(log p) — para a pilha de recursão do insertion_sort.
        4. Loop de impressão dos top_n plataformas:
        Tempo: O(top_n) — geralmente pequeno e constante (ex: 5 ou 10).
        Espaço: O(1) — apenas variáveis temporárias.
        5. Total:
        Tempo: O(n + n * m + p log p + top_n) — onde
        n é o número de conteúdos, m é o número de interações por conteúdo e p é o número de plataformas distintas.
        Espaço: O(n + p) — para armazenar as interações e plataformas.

        """

        plataformas = defaultdict(list)

        for conteudo in self._arvore_conteudos.percurso_em_ordem():
            for interacao in conteudo.interacoes:
                plataformas[interacao.plataforma_interacao.nome_plataforma].append(interacao.watch_duration_seconds)

        # Calcula a média de consumo para cada plataforma
        medias = {nome: sum(duracoes) / len(duracoes) for nome, duracoes in plataformas.items()}

        # Ordena as plataformas pela média de consumo (decrescente)
        plataformas_ordenadas = insertion_sort(list(medias.items()), key_func=lambda x: x[1])

        print(f"\nTop {top_n} plataformas por tempo médio de consumo:")
        for i, (nome, media) in enumerate(plataformas_ordenadas[:top_n], 1):
            print(f"{i}. {nome} - {media:.2f} segundos")
        
        return plataformas_ordenadas[:top_n] if top_n else plataformas_ordenadas

    def identificar_quantidade_comentarios_por_conteudo(self, top_n=5):
        """
        Identifica a quantidade de comentários por conteúdo e imprime os top_n conteúdos com mais comentários.
        Parâmetros:
        - top_n: número de conteúdos a serem retornados (se None, retorna todos).
        Retorna:
        - Lista dos conteúdos ordenados pela quantidade de comentários.
        ⏱️ Análise de Complexidade
        1. percurso_em_ordem() da árvore de conteúdos:
        Tempo: O(n) — onde n é o número de conteúdos na árvore.
        Espaço: O(n) — para armazenar a lista de conteúdos.
        2. Loop para contar comentários por conteúdo:
        Tempo: O(n) — onde n é o número total de conteúdos.
        Espaço: O(m) — onde m é o número de conteúdos distintos.
        3. insertion_sort(conteudos.items(), key_func):
        Tempo médio: O(m log m) — onde m é o número de conteúdos distintos.
        Tempo pior caso: O(m²) — se a lista já estiver ordenada ou quase ordenada.
        Espaço: O(log m) — para a pilha de recursão do insertion_sort.
        4. Loop de impressão dos top_n conteúdos:
        Tempo: O(top_n) — geralmente pequeno e constante (ex: 5 ou 10).
        Espaço: O(1) — apenas variáveis temporárias.
        5. Total:
        Tempo: O(n + n + m log m + top_n) — onde n é o número de conteúdos,
        m é o número de comentários por conteúdo e m é o número de conteúdos distintos.
        Espaço: O(n + m) — para armazenar as interações e conteúdos.

        """
            
        conteudos = self._arvore_conteudos.percurso_em_ordem()
        
        comentarios_por_conteudo = defaultdict(int)

        for conteudo in conteudos:
            for interacao in conteudo.interacoes:
                if interacao.tipo_interacao == "comment":
                    comentarios_por_conteudo[conteudo.nome_conteudo] += 1

        # Ordena os conteúdos pelo número de comentários (decrescente)
        conteudos_ordenados = insertion_sort(list(comentarios_por_conteudo.items()), key_func=lambda x: x[1])

        print(f"\nTop {top_n} conteúdos por quantidade de comentários:")
        for i, (nome, total) in enumerate(conteudos_ordenados[:top_n], 1):
            print(f"{i}. {nome} - {total} comentários")
            # imprimir os comentários de cada conteúdo
        for conteudo in self._arvore_conteudos.percurso_em_ordem():
            print(f"Conteúdo: {conteudo.nome_conteudo} (ID: {conteudo.id_conteudo})")
            

            
        return conteudos_ordenados[:top_n] if top_n else conteudos_ordenados