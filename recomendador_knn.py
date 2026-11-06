from heapq import nsmallest

from gerar_grafo import LIMIAR_DUPLICATA


class RecomendadorKNN:

    def __init__(self, musicas):
        self.musicas = musicas

    def _distancias(self, musica_referencia, expoente=1):
        for musica in self.musicas:
            if musica == musica_referencia:
                continue

            distancia = musica_referencia.calcula_distancia(musica, expoente=expoente)
            if distancia >= LIMIAR_DUPLICATA:
                yield musica, distancia

    def recomendar(self, musica_referencia, k=5, expoente=1):
        if k <= 0:
            raise ValueError("k deve ser maior que zero.")

        return nsmallest( # retorna uma lista com os n menores elementos de um iterável, ordenados de forma ascendente (do menor para o maior).
            k,
            self._distancias(musica_referencia, expoente),
            key=lambda item: item[1],
        )

    def gerar_sequencia_suave(self, musica_inicial, tamanho=5, expoente=1):
        """Gera uma playlist encadeada aplicando a função de custo/suavização no kNN."""
        sequencia = [musica_inicial]
        visitadas = {musica_inicial}
        atual = musica_inicial

        for _ in range(tamanho):
            candidatos = []
            for m in self.musicas:
                if m in visitadas:
                    continue
                d = atual.calcula_distancia(m, expoente=expoente)
                if d >= LIMIAR_DUPLICATA:
                    candidatos.append((m, d))

            if not candidatos:
                break

            proxima, dist = min(candidatos, key=lambda item: item[1])
            sequencia.append((proxima, dist))
            visitadas.add(proxima)
            atual = proxima

        return sequencia