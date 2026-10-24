import math

# Faixas usadas para normalizar o tempo e o loudness para 0-1
TEMPO_MIN, TEMPO_MAX = 40.319, 209.816
LOUDNESS_MIN, LOUDNESS_MAX = -27.145, -1.192  # confira com os seus dados (veja abaixo)

# Pesos de cada característica na distância
PESO_DANCEABILITY = 1.0
PESO_ENERGY = 1.5
PESO_VALENCE = 1.0
PESO_TEMPO = 0.3          # baixo: a detecção de BPM às vezes erra pelo dobro
PESO_ACOUSTICNESS = 1.5
PESO_INSTRUMENTALNESS = 0.8
PESO_LOUDNESS = 1.0
PESO_SPEECHINESS = 0.5
PESO_LIVENESS = 0.2       # baixo: o modelo é ruidoso nesta característica


def normaliza(valor, minimo, maximo):
    # leva o valor para 0-1, cortando o que passar dos limites
    v = (valor - minimo) / (maximo - minimo)
    return max(0.0, min(1.0, v))


class Musica:

    def __init__(self, id_spotify, nome, artista, danceability, energy, valence, tempo, acousticness, instrumentalness, loudness, speechiness, liveness):
        self.id = id_spotify
        self.nome = nome
        self.artista = artista

        self.danceability = float(danceability)
        self.energy = float(energy)
        self.valence = float(valence)
        self.tempo = normaliza(float(tempo), TEMPO_MIN, TEMPO_MAX)
        self.acousticness = float(acousticness)
        self.instrumentalness = float(instrumentalness)
        self.loudness = normaliza(float(loudness), LOUDNESS_MIN, LOUDNESS_MAX)
        self.speechiness = float(speechiness)
        self.liveness = float(liveness)

    def __repr__(self):
        return f"{self.nome} - {self.artista}"

    def __eq__(self, outro):
        return isinstance(outro, Musica) and self.id == outro.id

    def __hash__(self):
        return hash(self.id)

    def calcula_distancia(self, m2):
        distance_danceability = PESO_DANCEABILITY * (self.danceability - m2.danceability) ** 2
        distance_energy = PESO_ENERGY * (self.energy - m2.energy) ** 2
        distance_valence = PESO_VALENCE * (self.valence - m2.valence) ** 2
        distance_tempo = PESO_TEMPO * (self.tempo - m2.tempo) ** 2
        distance_acousticness = PESO_ACOUSTICNESS * (self.acousticness - m2.acousticness) ** 2
        distance_instrumentalness = PESO_INSTRUMENTALNESS * (self.instrumentalness - m2.instrumentalness) ** 2
        distance_loudness = PESO_LOUDNESS * (self.loudness - m2.loudness) ** 2
        distance_speechiness = PESO_SPEECHINESS * (self.speechiness - m2.speechiness) ** 2
        distance_liveness = PESO_LIVENESS * (self.liveness - m2.liveness) ** 2

        return math.sqrt(
            distance_danceability + distance_energy + distance_valence + distance_tempo
            + distance_acousticness + distance_instrumentalness + distance_loudness
            + distance_speechiness + distance_liveness
        )

    