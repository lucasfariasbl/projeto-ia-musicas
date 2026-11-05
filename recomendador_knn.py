from heapq import nsmallest

from gerar_grafo import LIMIAR_DUPLICATA


class RecomendadorKNN:

    def __init__(self, musicas):
        self.musicas = musicas

    def _distancias(self, musica_referencia, expoente=1):
        for musica in self.musicas:
            if musica == musica_referencia:
                continue

            distancia = musica_referencia.calcula_distancia(musica)
            if distancia >= LIMIAR_DUPLICATA:
                # O expoente 2 penaliza distâncias maiores no ranqueamento
                custo = distancia ** expoente
                yield musica, distancia, custo

    def recomendar(self, musica_referencia, k=5, expoente=1):
        if k <= 0:
            raise ValueError("k deve ser maior que zero.")

        # Ordena pelo custo penalizado (item[2]), mas mantém a distância original (item[1])
        ordenados = nsmallest(
            k,
            self._distancias(musica_referencia, expoente),
            key=lambda item: item[2],
        )
        return [(musica, dist) for musica, dist, _ in ordenados]

    def gerar_sequencia_suave(self, musica_inicial, tamanho=5, expoente=1):
        """Gera uma sequência encadeada onde cada música é a vizinha mais próxima da anterior."""
        sequencia = [musica_inicial]
        visitadas = {musica_inicial}
        atual = musica_inicial

        for _ in range(tamanho):
            candidatos = []
            for m in self.musicas:
                if m in visitadas:
                    continue
                d = atual.calcula_distancia(m)
                if d >= LIMIAR_DUPLICATA:
                    candidatos.append((m, d, d ** expoente))

            if not candidatos:
                break

            # Escolhe o próximo passo com base no menor custo (com expoente)
            proxima, dist, _ = min(candidatos, key=lambda item: item[2])
            sequencia.append((proxima, dist))
            visitadas.add(proxima)
            atual = proxima

        return sequencia