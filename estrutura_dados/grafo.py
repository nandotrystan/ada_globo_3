class Grafo:
    def __init__(self):
        self.adjacencias = {}

    def adicionar_vertice(self, vertice):
        if vertice not in self.adjacencias:
            self.adjacencias[vertice] = []

    def adicionar_aresta(self, origem, destino):
        if origem not in self.adjacencias:
            self.adicionar_vertice(origem)
        if destino not in self.adjacencias:
            self.adicionar_vertice(destino)
        self.adjacencias[origem].append(destino)

    def obter_adjacentes(self, vertice):
        return self.adjacencias.get(vertice, [])
    
    def __str__(self):
        resultado = []
        for vertice, adjacentes in self.adjacencias.items():
            resultado.append(f"{vertice} -> {', '.join(adjacentes)}")
        return "\n".join(resultado)
    
    def vertices(self):
        return list(self.adjacencias.keys())
    
    def arestas(self):
        arestas = []
        for origem, destinos in self.adjacencias.items():
            for destino in destinos:
                arestas.append((origem, destino))
        return arestas
    
    def eh_vazio(self):
        return len(self.adjacencias) == 0
    
    def limpar(self):
        self.adjacencias.clear()

    def __len__(self):
        return len(self.adjacencias)
    
    def __contains__(self, vertice):
        return vertice in self.adjacencias
    
    def __getitem__(self, vertice):
        return self.adjacencias.get(vertice, [])
    
    def __setitem__(self, vertice, destinos):
        if vertice not in self.adjacencias:
            self.adjacencias[vertice] = []
        self.adjacencias[vertice].extend(destinos)

    def __delitem__(self, vertice):
        if vertice in self.adjacencias:
            del self.adjacencias[vertice]
            for destinos in self.adjacencias.values():
                if vertice in destinos:
                    destinos.remove(vertice)

    def __contains__(self, item):
        return item in self.adjacencias or any(item in destinos for destinos in self.adjacencias.values())
    
    def __iter__(self):
        return iter(self.adjacencias.items())
    
    def __repr__(self):
        return f"Grafo({self.adjacencias})"
    
    def __eq__(self, other):
        if not isinstance(other, Grafo):
            return False
        return self.adjacencias == other.adjacencias
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __len__(self):
        return len(self.adjacencias)
    
    def __bool__(self):
        return not self.eh_vazio()
    
    def copy(self):
        novo_grafo = Grafo()
        novo_grafo.adjacencias = {vertice: destinos[:] for vertice, destinos in self.adjacencias.items()}
        return novo_grafo
    
    def to_dict(self):
        return {vertice: destinos[:] for vertice, destinos in self.adjacencias.items()}
    
    @classmethod
    def from_dict(cls, dicionario):
        grafo = cls()
        for vertice, destinos in dicionario.items():
            grafo.adicionar_vertice(vertice)
            for destino in destinos:
                grafo.adicionar_aresta(vertice, destino)
        return grafo
    
    def to_json(self):
        import json
        return json.dumps(self.to_dict(), indent=4)
    
    @classmethod
    def from_json(cls, json_str):
        import json
        dicionario = json.loads(json_str)
        return cls.from_dict(dicionario)
    
    def to_adjacency_matrix(self):
        vertices = self.vertices()
        tamanho = len(vertices)
        matriz = [[0] * tamanho for _ in range(tamanho)]
        
        for i, vertice in enumerate(vertices):
            for destino in self.obter_adjacentes(vertice):
                if destino in vertices:
                    j = vertices.index(destino)
                    matriz[i][j] = 1
        
        return matriz
    
    def __hash__(self):
        return hash(frozenset((vertice, tuple(destinos)) for vertice, destinos in self.adjacencias.items()))

    def sssp(self, no_inicial, limite=None):
        """
        Encontra os menores caminhos de um nó de partida para todos os nós alcançáveis.
        """
        if no_inicial not in self.adjacencias:
            return {}
        
        return self.__sssp(no_inicial, limite)
    
    def __sssp(self, no_inicial, limite):
        """
        Função auxiliar para encontrar o menor caminho usando uma abordagem similar a BFS.
        Adaptada para usar rótulos de nós arbitrários.
        """
        caminhos = {no_inicial: [no_inicial]}
        fila = [(no_inicial, 0)]
        while fila:
            no_atual, nivel = fila.pop(0)

            if limite is not None and nivel >= limite:
                continue
            
            for vizinho in self.obter_adjacentes(no_atual):
                if vizinho not in caminhos:
                    caminhos[vizinho] = caminhos[no_atual] + [vizinho]
                    fila.append((vizinho, nivel + 1))
        return caminhos
    
    
    @classmethod
    def from_adjacency_matrix(cls, matriz):
        grafo = cls()
        tamanho = len(matriz)
        vertices = [f"v{i}" for i in range(tamanho)]
        
        for i in range(tamanho):
            grafo.adicionar_vertice(vertices[i])
            for j in range(tamanho):
                if matriz[i][j] == 1:
                    grafo.adicionar_aresta(vertices[i], vertices[j])
        
        return grafo
    
    def to_edge_list(self):
        return [(origem, destino) for origem, destinos in self.adjacencias.items() for destino in destinos] 
    
    @classmethod
    def from_edge_list(cls, lista_arestas):
        grafo = cls()
        for origem, destino in lista_arestas:
            grafo.adicionar_aresta(origem, destino)
        return grafo
    
    def to_dot(self):
        dot_str = "digraph G {\n"
        for vertice, destinos in self.adjacencias.items():
            for destino in destinos:
                dot_str += f'    "{vertice}" -> "{destino}";\n'
        dot_str += "}\n"
        return dot_str
    
    @classmethod
    def from_dot(cls, dot_str):
        import re
        grafo = cls()
        padrao = r'"([^"]+)"\s*->\s*"([^"]+)"'
        arestas = re.findall(padrao, dot_str)
        
        for origem, destino in arestas:
            grafo.adicionar_aresta(origem, destino)
        
        return grafo
    

# Example usage:

if __name__ == "__main__":
    grafo = Grafo()
    grafo.adicionar_vertice("A")
    grafo.adicionar_vertice("B")
    grafo.adicionar_aresta("A", "B")
    grafo.adicionar_aresta("A", "C")
    grafo.adicionar_aresta("B", "C")
    grafo.adicionar_aresta("C", "D")
    print(grafo)
    print("Vértices:", grafo.vertices())
    print("Arestas:", grafo.arestas())
    print("Adjacentes de A:", grafo.obter_adjacentes("A"))
    print("Matriz de adjacência:")
    for linha in grafo.to_adjacency_matrix():
        print(linha)
    print("Lista de arestas:", grafo.to_edge_list())
    print("Representação DOT:")
    print(grafo.to_dot())
    grafo_json = grafo.to_json()
    print("Grafo em JSON:")
    print(grafo_json)
    grafo_copiado = grafo.copy()
    print("Grafo copiado:")
    print(grafo_copiado)
    grafo_limpo = grafo.copy()
    grafo_limpo.limpar()
    print("Grafo após limpeza:")
    print(grafo_limpo)
    print("Grafo original ainda existe:")
    print(grafo)
    print("Grafo vazio:", grafo_limpo.eh_vazio())
    grafo_json_str = grafo.to_json()
    grafo_from_json = Grafo.from_json(grafo_json_str)
    print("Grafo criado a partir do JSON:")
    print(grafo_from_json)
    grafo_dot_str = grafo.to_dot()
    grafo_from_dot = Grafo.from_dot(grafo_dot_str)
    print("Grafo criado a partir da representação DOT:")
    print(grafo_from_dot)
    matriz = grafo.to_adjacency_matrix()
    grafo_from_matrix = Grafo.from_adjacency_matrix(matriz)
    print("Grafo criado a partir da matriz de adjacência:")
    print(grafo_from_matrix)
    lista_arestas = grafo.to_edge_list()
    grafo_from_edge_list = Grafo.from_edge_list(lista_arestas)
    print("Grafo criado a partir da lista de arestas:")
    print(grafo_from_edge_list)
    print("Grafo é igual ao grafo copiado:", grafo == grafo_copiado)
    print("Grafo é diferente do grafo limpo:", grafo != grafo_limpo)
    print("Grafo contém 'A':", "A" in grafo)
    print("Grafo contém 'E':", "E" in grafo)
    print("Grafo contém aresta 'A' -> 'B':", ("A", "B") in grafo.arestas())
    print("Grafo contém aresta 'B' -> 'A':", ("B", "A") in grafo.arestas())
    print("Iterando sobre o grafo:")
    for vertice, destinos in grafo:
        print(f"{vertice} -> {', '.join(destinos)}")
    print("Representação do grafo:", repr(grafo))
    print("Tamanho do grafo:", len(grafo))
    print("Grafo é vazio:", grafo.eh_vazio())
    
    print("Grafo é não vazio:", not grafo.eh_vazio())
    print("Grafo é booleano:", bool(grafo))
    print("Grafo limpo é booleano:", bool(grafo_limpo))
    print("Grafo contém 'A':", 'A' in grafo)
    print("Grafo contém 'E':", 'E' in grafo)
    print("Grafo contém aresta 'A' -> 'B':", ('A',  'B') in grafo.arestas())
    print("Grafo contém aresta 'B' -> 'A':", ('B', 'A') in grafo.arestas())

# procurar o menor caminho de um nó de partida para todos os nós alcançáveis

    print("Menor caminho a partir de 'A':", grafo.sssp("A"))
    print("Menor caminho a partir de 'B':", grafo.sssp("B"))
    print("Menor caminho a partir de 'C':", grafo.sssp("C"))
    print("Menor caminho a partir de 'D':", grafo.sssp("D"))
    print("Menor caminho a partir de 'E':", grafo.sssp("E"))
    print("Menor caminho a partir de 'A' com limite 1:", grafo.sssp("A", limite=1))
    print("Menor caminho a partir de 'A' com limite 2:", grafo.sssp("A", limite=2))
    print("Menor caminho a partir de 'B' com limite 1:", grafo.sssp("B", limite=1))
    print("Menor caminho a partir de 'B' com limite 2:", grafo.sssp("B", limite=2))
    print("Menor caminho a partir de 'C' com limite 1:", grafo.sssp("C", limite=1))
    print("Menor caminho a partir de 'C' com limite 2:", grafo.sssp("C", limite=2))
    print("Menor caminho a partir de 'D' com limite 1:", grafo.sssp("D", limite=1))
    print("Menor caminho a partir de 'D' com limite 2:", grafo.sssp("D", limite=2))
    print("Menor caminho a partir de 'E' com limite 1:", grafo.sssp("E", limite=1))
    print("Menor caminho a partir de 'E' com limite 2:", grafo.sssp("E", limite=2))
    print("Menor caminho a partir de 'A' com limite 3:", grafo.sssp("A", limite=3))
    print("Menor caminho a partir de 'B' com limite 3:", grafo.sssp("B", limite=3))
    print("Menor caminho a partir de 'C' com limite 3:", grafo.sssp("C", limite=3))
    print("Menor caminho a partir de 'D' com limite 3:", grafo.sssp("D", limite=3))
    print("Menor caminho a partir de 'E' com limite 3:", grafo.sssp("E", limite=3))