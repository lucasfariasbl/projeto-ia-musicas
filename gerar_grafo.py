import pandas as pd
import re
from musica import Musica
from grafo import Grafo

def construir_grafo(csv_path, k_vizinhos=10):
    grafo = Grafo()
    lista_musicas = []

    # leitura do csv com as músicas
    df = pd.read_csv(csv_path)

    # um nó por música: versões repetidas viram uma só (o csv não é alterado)
    df["_chave"] = df["nome"].map(normaliza_texto) + "|" + df["artista"].map(normaliza_texto)
    df = df.drop_duplicates(subset="_chave", keep="first").drop(columns="_chave")

    # instanciacao das musicas
    for _, row in df.iterrows():
        nova_musica = Musica(
            id_spotify=row['id'],
            nome=row['nome'],
            artista=row['artista'],
            danceability=row['danceability'],
            energy=row['energy'],
            valence=row['valence'],
            tempo=row['tempo'],
            acousticness=row['acousticness'],
            instrumentalness=row['instrumentalness'],
            loudness=row['loudness'],
            speechiness=row['speechiness'],
            liveness=row['liveness'],
        )

        lista_musicas.append(nova_musica)
        grafo.adiciona_musica(nova_musica)


    cache_distancias = {}

    # calculo das 10 musicas mais proximas à selecionada
    for origem in lista_musicas:
        distancias = []

        for destino in lista_musicas:
            if origem.id == destino.id:
                continue

            par = frozenset([origem, destino])
            
            # Verifica a cache antes de invocar o processamento matemático
            if par not in cache_distancias:
                cache_distancias[par] = origem.calcula_distancia(destino)

            peso = cache_distancias[par]

            if peso < 0.001:
                continue

            distancias.append((destino, peso))

        distancias.sort(key=lambda x: x[1])
        top_k = distancias[:k_vizinhos]

        # insercao das arestas no grafo
        for vizinho, peso in top_k:
            grafo.conecta_musicas(origem, vizinho, peso)

    return grafo, lista_musicas

def normaliza_texto(texto):
    # tira sufixos de versão e parênteses para comparar nomes
    texto = str(texto).lower().strip()
    texto = re.sub(r"\s*[-–]\s*(remaster(ed)?|single version|album version|radio edit|mono|stereo|\d{4}).*$", "", texto)
    texto = re.sub(r"\s*[\(\[].*?[\)\]]", "", texto)
    return texto.strip()