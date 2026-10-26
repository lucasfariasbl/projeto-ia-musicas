import pickle
from pathlib import Path

from gerar_grafo import construir_grafo

BASE = Path(__file__).resolve().parent
CAMINHO_CSV = BASE / "data" / "playlist.csv"
CAMINHO_PKL = BASE / "data" / "grafo_cache.pkl"

K_VIZINHOS = 10
VERSAO_CACHE = 3  # aumente se mudar a estrutura de Grafo/Musica


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

    # usa o cache só se for da mesma versão/CSV; qualquer erro => regenera
    if CAMINHO_PKL.exists():
        try:
            with open(CAMINHO_PKL, "rb") as arquivo:
                cache = pickle.load(arquivo)
            if _cache_valido(cache):
                return cache["grafo"], cache["playlist"]
        except Exception:
            pass

    print("Gerando o grafo...")
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


def mostrar_caminho(grafo, origem, destino, expoente):
    caminho, custo = grafo.dijkstra(origem, destino, expoente)

    print(f"\n=== Dijkstra (expoente={expoente}) ===")
    if caminho is None:
        print("Não existe caminho entre as duas músicas.")
        return

    saltos = grafo.pesos_do_caminho(caminho)
    print(f"Custo total: {custo:.4f} | Músicas: {len(caminho)}", end="")
    if saltos:
        print(f" | Maior salto: {max(saltos):.4f} | Salto médio: {sum(saltos) / len(saltos):.4f}")
    else:
        print()

    for i, musica in enumerate(caminho):
        salto = f" (salto {saltos[i - 1]:.4f})" if i > 0 else ""
        print(f" {i + 1:>2}. {musica}{salto}")


if __name__ == "__main__":
    grafo_playlist, playlist = carregar_grafo()

    if len(playlist) < 2:
        raise SystemExit("A playlist precisa de pelo menos 2 músicas.")

    componentes = grafo_playlist.componentes_conexos()
    print(f"Músicas: {len(playlist)} | Componentes conexos: {len(componentes)}"
          f" | Maior componente: {len(componentes[0])}")

    origem = playlist[min(288, len(playlist) - 1)]
    destino = playlist[0] if origem != playlist[0] else playlist[-1]

    print(f"\nOrigem: {origem}\nDestino: {destino}")

    # compara soma simples com custo ao quadrado
    for expoente in (1, 2):
        mostrar_caminho(grafo_playlist, origem, destino, expoente)