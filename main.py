import pickle
from pathlib import Path

from gerar_grafo import construir_grafo

BASE = Path(__file__).resolve().parent
CAMINHO_CSV = BASE / "data" / "playlist.csv"
CAMINHO_PKL = BASE / "data" / "grafo_cache.pkl"


def carregar_grafo():
    # se o grafo já foi gerado antes, só carrega do disco
    if CAMINHO_PKL.exists():
        with open(CAMINHO_PKL, "rb") as arquivo:
            return pickle.load(arquivo)

    # senão, gera a partir do csv e guarda para as próximas execuções
    print("Gerando o grafo (primeira execução)...")
    grafo, playlist = construir_grafo(CAMINHO_CSV)

    CAMINHO_PKL.parent.mkdir(exist_ok=True)
    with open(CAMINHO_PKL, "wb") as arquivo:
        pickle.dump((grafo, playlist), arquivo)

    return grafo, playlist


if __name__ == "__main__":
    grafo_playlist, playlist = carregar_grafo()

    musica_teste = playlist[288]
    vizinhos = grafo_playlist.obter_vizinhos(musica_teste)

    print(f"\nVizinhos de '{musica_teste}':")

    vizinhos_ordenados = sorted(vizinhos.items(), key=lambda item: item[1])

    for vizinho, peso in vizinhos_ordenados:
        print(f" -> {vizinho} | Custo: {peso:.4f}")