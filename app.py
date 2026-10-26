import random

import pandas as pd
import streamlit as st

from main import carregar_grafo
from recomendador_knn import RecomendadorKNN

st.set_page_config(page_title="Transição entre músicas", layout="wide")

EXPOENTES = {
    1: "Soma simples (expoente 1)",
    2: "Custo ao quadrado (expoente 2)",
}


@st.cache_resource(show_spinner="Carregando o grafo...")
def carregar():
    grafo, playlist = carregar_grafo()
    return grafo, playlist, RecomendadorKNN(playlist)


try:
    grafo, playlist, knn = carregar()
except Exception as erro:
    st.error(f"Não foi possível carregar o grafo: {erro}")
    st.stop()

# opções do seletor: índices da playlist em ordem alfabética
ordem = sorted(range(len(playlist)), key=lambda i: str(playlist[i]).lower())


def rotulo(i):
    return str(playlist[i])


def sortear():
    a, b = random.sample(range(len(playlist)), 2)
    st.session_state.origem = a
    st.session_state.destino = b


if "origem" not in st.session_state:
    sortear()

# ---------------------------------------------------------------- cabeçalho
st.title("Sequência de músicas por busca em grafo")
st.caption(
    "Cada música é um nó, ligado às mais parecidas em características de áudio. "
    "O Dijkstra encontra o caminho da música inicial até a música alvo, "
    "passando por faixas semelhantes."
)

col_a, col_b, col_c = st.columns([5, 5, 2])
with col_a:
    st.selectbox("Música inicial", ordem, format_func=rotulo, key="origem")
with col_b:
    st.selectbox("Música alvo", ordem, format_func=rotulo, key="destino")
with col_c:
    st.write("")
    st.write("")
    st.button("Sortear par", on_click=sortear)

origem = playlist[st.session_state.origem]
destino = playlist[st.session_state.destino]

aba_caminho, aba_similares = st.tabs(["Sequência (Dijkstra)", "Músicas similares (kNN)"])

# ---------------------------------------------------------------- caminho
with aba_caminho:
    if origem == destino:
        st.info("Escolha músicas diferentes para gerar a sequência.")
    else:
        resultados = {e: grafo.dijkstra(origem, destino, e) for e in EXPOENTES}

        if any(caminho is None for caminho, _ in resultados.values()):
            st.warning("Não existe caminho entre essas duas músicas no grafo.")
        else:
            direta = origem.calcula_distancia(destino)
            st.metric(
                "Distância direta entre origem e alvo",
                f"{direta:.4f}",
                help="Seria o tamanho do 'salto' se a transição fosse feita de uma vez só.",
            )

            saltos_por_expoente = {}
            colunas = st.columns(len(EXPOENTES))

            for coluna, (expoente, titulo) in zip(colunas, EXPOENTES.items()):
                caminho, custo = resultados[expoente]
                saltos = grafo.pesos_do_caminho(caminho)
                saltos_por_expoente[titulo] = pd.Series(saltos, index=range(1, len(saltos) + 1))

                with coluna:
                    st.subheader(titulo)
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Músicas", len(caminho))
                    m2.metric("Maior salto", f"{max(saltos):.4f}")
                    m3.metric("Salto médio", f"{sum(saltos) / len(saltos):.4f}")

                    tabela = pd.DataFrame({
                        "#": range(1, len(caminho) + 1),
                        "Música": [m.nome for m in caminho],
                        "Artista": [m.artista for m in caminho],
                        "Salto": [None] + [round(s, 4) for s in saltos],
                    })
                    st.dataframe(tabela, hide_index=True)

            st.subheader("Tamanho de cada salto ao longo da sequência")
            st.caption("Quanto mais baixa e uniforme a linha, mais suave é a transição.")
            st.line_chart(pd.DataFrame(saltos_por_expoente))

            st.subheader("Características de áudio ao longo da sequência")
            escolhido = st.radio(
                "Sequência exibida",
                list(EXPOENTES),
                format_func=lambda e: EXPOENTES[e],
                horizontal=True,
            )
            caminho = resultados[escolhido][0]
            caracteristicas = pd.DataFrame(
                [m.caracteristicas for m in caminho],
                index=range(1, len(caminho) + 1),
            )
            st.line_chart(caracteristicas)
            st.caption("Tempo e loudness estão normalizados entre 0 e 1.")

# ---------------------------------------------------------------- kNN
with aba_similares:
    st.write("As k músicas mais próximas da música inicial, calculadas direto pelo kNN.")
    k = st.slider("Quantidade de músicas (k)", 1, 20, 5)

    similares = knn.recomendar(origem, k)
    st.dataframe(
        pd.DataFrame({
            "Música": [m.nome for m, _ in similares],
            "Artista": [m.artista for m, _ in similares],
            "Distância": [round(d, 4) for _, d in similares],
        }),
        hide_index=True,
    )