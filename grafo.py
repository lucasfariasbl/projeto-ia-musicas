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