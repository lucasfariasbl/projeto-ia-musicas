from heapq import nsmallest

from gerar_grafo import LIMIAR_DUPLICATA


class RecomendadorKNN:

    def __init__(self, musicas):
        self.musicas = musicas

    def _distancias(self, musica_referencia):
        # calcula cada distância uma vez só e descarta a própria música
        # e as quase-duplicatas (mesmo critério usado no grafo)
        for musica in self.musicas:
            if musica == musica_referencia:
                continue

            distancia = musica_referencia.calcula_distancia(musica)
            if distancia >= LIMIAR_DUPLICATA:
                yield musica, distancia

    def recomendar(self, musica_referencia, k=5):
        if k <= 0:
            raise ValueError("k deve ser maior que zero.")

        return nsmallest(
            k,
            self._distancias(musica_referencia),
            key=lambda item: item[1],
        )