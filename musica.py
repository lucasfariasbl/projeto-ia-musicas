import math

LIMITES = {
    "tempo": (40.319, 209.816),
    "loudness": (-27.145, -1.192),
}

PESOS = {
    "danceability": 1.0,
    "energy": 1.5,
    "valence": 1.0,
    "tempo": 0.3,          # baixo: BPM às vezes erra pelo dobro
    "acousticness": 1.5,
    "instrumentalness": 0.8,
    "loudness": 1.0,
    "speechiness": 0.5,
    "liveness": 0.2,       # baixo: modelo ruidoso
}

def normaliza(valor, minimo, maximo):
    v = (valor - minimo) / (maximo - minimo)
    return max(0.0, min(1.0, v))

class Musica:

    def __init__(self, id_spotify, nome, artista, **dados):
        self.id = id_spotify
        self.nome = nome
        self.artista = artista

        self.caracteristicas = {}
        for chave in PESOS:
            valor = float(dados[chave])
            if chave in LIMITES:
                valor = normaliza(valor, *LIMITES[chave])
            self.caracteristicas[chave] = valor

    def __repr__(self):
        return f"{self.nome} - {self.artista}"

    def __eq__(self, outro):
        return isinstance(outro, Musica) and self.id == outro.id

    def __hash__(self):
        return hash(self.id)

    def calcula_distancia(self, m2):
        return math.sqrt(sum(
            peso * (self.caracteristicas[c] - m2.caracteristicas[c]) ** 2
            for c, peso in PESOS.items()
        ))