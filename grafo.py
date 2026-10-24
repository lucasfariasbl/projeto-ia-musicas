class Grafo:

    def __init__(self):
        self.adjacencias = {}

    def adiciona_musica(self, musica):
        if musica not in self.adjacencias:
            self.adjacencias[musica] = {}

    def conecta_musicas(self, m1, m2, peso):
        self.adjacencias[m1][m2] = peso
        self.adjacencias[m2][m1] = peso

    def obter_vizinhos(self, musica):
        return self.adjacencias.get(musica, {})

    # def dijkstra (final boss)