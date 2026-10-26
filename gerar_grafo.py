import re

import numpy as np
import pandas as pd

from grafo import Grafo
from musica import Musica, PESOS

LIMIAR_DUPLICATA = 0.001

COLUNAS_OBRIGATORIAS = ["id", "nome", "artista", *PESOS]


def normaliza_texto(texto):
    # tira sufixos de versão e parênteses para comparar nomes
    original = str(texto).lower().strip()
    t = re.sub(r"\s*[-–]\s*(remaster(ed)?|single version|album version|radio edit|mono|stereo|\d{4}).*$", "", original)
    t = re.sub(r"\s*[\(\[].*?[\)\]]", "", t).strip()
    # se sobrou nada (ex.: título só entre parênteses), usa o original
    return t or original


def carregar_dataframe(csv_path):
    df = pd.read_csv(csv_path)

    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    if faltando:
        raise ValueError(f"O CSV não tem as colunas: {faltando}")

    # garante que as características são numéricas; lixo vira NaN
    for c in PESOS:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # descarta linhas incompletas (NaN quebraria as distâncias)
    df = df.dropna(subset=COLUNAS_OBRIGATORIAS).copy()

    # mesmo id duas vezes colapsaria no dict do grafo
    df = df.drop_duplicates(subset="id")

    # remove versões repetidas da mesma música
    chave = df["nome"].map(normaliza_texto) + "|" + df["artista"].map(normaliza_texto)
    df = df[~chave.duplicated()]

    return df.rename(columns={"id": "id_spotify"})


def construir_grafo(csv_path, k_vizinhos=10):
    df = carregar_dataframe(csv_path)

    lista_musicas = [Musica(**linha) for linha in df.to_dict("records")]

    grafo = Grafo()
    for musica in lista_musicas:
        grafo.adiciona_musica(musica)

    n = len(lista_musicas)
    if n < 2:
        return grafo, lista_musicas

    # matriz n x 9 já multiplicada por sqrt(peso): a distância euclidiana
    # entre linhas é exatamente Musica.calcula_distancia
    X = np.array([[m.caracteristicas[c] for c in PESOS] for m in lista_musicas])
    X = X * np.sqrt(np.array(list(PESOS.values())))

    # uma linha por vez: memória O(n) em vez de guardar todos os n² pares
    for i in range(n):
        d = np.sqrt(((X - X[i]) ** 2).sum(axis=1))
        d[i] = np.inf                    # não liga a música a ela mesma
        d[d < LIMIAR_DUPLICATA] = np.inf  # ignora quase-duplicatas

        validos = np.flatnonzero(np.isfinite(d))
        if validos.size == 0:
            continue
        if validos.size > k_vizinhos:
            escolhidos = validos[np.argpartition(d[validos], k_vizinhos - 1)[:k_vizinhos]]
        else:
            escolhidos = validos

        for j in escolhidos:
            grafo.conecta_musicas(lista_musicas[i], lista_musicas[j], float(d[j]))

    return grafo, lista_musicas