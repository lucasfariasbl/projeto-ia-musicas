import re
from heapq import nsmallest

import pandas as pd

from grafo import Grafo
from musica import Musica

LIMIAR_DUPLICATA = 0.001

def normaliza_texto(texto):
    # tira sufixos de versão e parênteses para comparar nomes
    texto = str(texto).lower().strip()
    texto = re.sub(r"\s*[-–]\s*(remaster(ed)?|single version|album version|radio edit|mono|stereo|\d{4}).*$", "", texto)
    texto = re.sub(r"\s*[\(\[].*?[\)\]]", "", texto)
    return texto.strip()

def construir_grafo(csv_path, k_vizinhos=10):
    df = pd.read_csv(csv_path)

    chave = df["nome"].map(normaliza_texto) + "|" + df["artista"].map(normaliza_texto)
    df = df[~chave.duplicated()]

    df = df.rename(columns={"id": "id_spotify"})
    lista_musicas = [Musica(**linha) for linha in df.to_dict("records")]

    grafo = Grafo()
    for musica in lista_musicas:
        grafo.adiciona_musica(musica)


    candidatos = {m: [] for m in lista_musicas}

    for i, a in enumerate(lista_musicas):
        for b in lista_musicas[i + 1:]:
            peso = a.calcula_distancia(b)
            
            if peso < LIMIAR_DUPLICATA:
                continue
            
            candidatos[a].append((b, peso))
            candidatos[b].append((a, peso))

    for origem, lista in candidatos.items():
        for vizinho, peso in nsmallest(k_vizinhos, lista, key=lambda x: x[1]):
            grafo.conecta_musicas(origem, vizinho, peso)

    return grafo, lista_musicas