import pickle
from pathlib import Path

from gerar_grafo import construir_grafo

BASE = Path(__file__).resolve().parent
CAMINHO_CSV = BASE / "data" / "playlist.csv"
CAMINHO_PKL = BASE / "data" / "grafo_cache.pkl"

K_VIZINHOS = 10
VERSAO_CACHE = 4  # Incremente para invalidar o cache antigo


def _cache_valido(cache):
    return (
        isinstance(cache, dict)
        and cache.get("versao") == VERSAO_CACHE
        and cache.get("k") == K_VIZINHOS
        and cache.get("csv_mtime") == CAMINHO_CSV.stat().st_mtime
    )


def carregar_grafo():
    if not CAMINHO_CSV.exists():
        raise FileNotFoundError(f"CSV não encontrado: {CAMINHO_CSV}")

    if CAMINHO_PKL.exists():
        try:
            with open(CAMINHO_PKL, "rb") as arquivo:
                cache = pickle.load(arquivo)
            if _cache_valido(cache):
                return cache["grafo"], cache["playlist"]
        except Exception:
            pass

    print("Gerando a base de dados...")
    grafo, playlist = construir_grafo(CAMINHO_CSV, K_VIZINHOS)

    CAMINHO_PKL.parent.mkdir(parents=True, exist_ok=True)
    with open(CAMINHO_PKL, "wb") as arquivo:
        pickle.dump({
            "versao": VERSAO_CACHE,
            "k": K_VIZINHOS,
            "csv_mtime": CAMINHO_CSV.stat().st_mtime,
            "grafo": grafo,
            "playlist": playlist,
        }, arquivo)

    return grafo, playlist


if __name__ == "__main__":
    grafo_playlist, playlist = carregar_grafo()

    if len(playlist) < 2:
        raise SystemExit("A playlist precisa de pelo menos 2 músicas.")

    componentes = grafo_playlist.componentes_conexos()
    print(f"Músicas: {len(playlist)} | Componentes conexos: {len(componentes)}"