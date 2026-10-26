import heapq
from itertools import count


class Grafo:

    def __init__(self):
        self.adjacencias = {}

    def adiciona_musica(self, musica):
        if musica not in self.adjacencias:
            self.adjacencias[musica] = {}

    def conecta_musicas(self, m1, m2, peso):
        self.adjacencias.setdefault(m1, {})[m2] = peso
        self.adjacencias.setdefault(m2, {})[m1] = peso

    def obter_vizinhos(self, musica):
        return self.adjacencias.get(musica, {})

    def dijkstra(self, origem, destino, expoente=1):
        """
        Caminho de menor custo entre duas músicas.

        O custo de cada aresta é peso ** expoente:
          - expoente=1: soma simples das distâncias
          - expoente=2: penaliza saltos grandes, favorecendo vários
            passos pequenos (transição mais suave)

        Retorna (caminho, custo_total), onde caminho é a lista de músicas
        de origem a destino. Se não houver caminho, retorna (None, inf).
        """
        if origem not in self.adjacencias:
            raise ValueError(f"Música de origem fora do grafo: {origem}")
        if destino not in self.adjacencias:
            raise ValueError(f"Música de destino fora do grafo: {destino}")
        if expoente <= 0:
            raise ValueError("expoente deve ser maior que zero.")

        if origem == destino:
            return [origem], 0.0

        custos = {origem: 0.0}
        anterior = {}
        visitados = set()

        # o contador desempata custos iguais sem precisar comparar Musicas
        desempate = count()
        fila = [(0.0, next(desempate), origem)]

        while fila:
            custo_atual, _, atual = heapq.heappop(fila)

            if atual in visitados:
                continue
            visitados.add(atual)

            if atual == destino:
                break

            for vizinho, peso in self.adjacencias[atual].items():
                if vizinho in visitados:
                    continue

                novo_custo = custo_atual + peso ** expoente
                if novo_custo < custos.get(vizinho, float("inf")):
                    custos[vizinho] = novo_custo
                    anterior[vizinho] = atual
                    heapq.heappush(fila, (novo_custo, next(desempate), vizinho))

        if destino not in visitados:
            return None, float("inf")

        caminho = [destino]
        while caminho[-1] != origem:
            caminho.append(anterior[caminho[-1]])
        caminho.reverse()

        return caminho, custos[destino]

    def pesos_do_caminho(self, caminho):
        """Distância original de cada salto do caminho (sem o expoente)."""
        return [self.adjacencias[a][b] for a, b in zip(caminho, caminho[1:])]

    def componentes_conexos(self):
        """Lista de conjuntos de músicas mutuamente alcançáveis, do maior ao menor."""
        restantes = set(self.adjacencias)
        componentes = []

        while restantes:
            inicio = restantes.pop()
            componente = {inicio}
            pilha = [inicio]

            while pilha:
                atual = pilha.pop()
                for vizinho in self.adjacencias[atual]:
                    if vizinho not in componente:
                        componente.add(vizinho)
                        pilha.append(vizinho)

            restantes -= componente
            componentes.append(componente)

        componentes.sort(key=len, reverse=True)
        return componentes