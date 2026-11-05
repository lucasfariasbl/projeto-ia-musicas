import random

import pandas as pd
import streamlit as st

from main import carregar_grafo
from recomendador_knn import RecomendadorKNN

st.set_page_config(page_title="Recomendador de Músicas", layout="wide")

EXPOENTES = {
    1: "Distância Linear (expoente 1)",
    2: "Penalizar Saltos Grandes (expoente 2)",
}


@st.cache_resource(show_spinner="Carregando dados...")
def carregar():
    grafo, playlist = carregar_grafo()
    return grafo, playlist, RecomendadorKNN(playlist)


try:
    grafo, playlist, knn = carregar()
except Exception as erro:
    st.error(f"Não foi possível carregar os dados: {erro}")
    st.stop()

ordem = sorted(range(len(playlist)), key=lambda i: str(playlist[i]).lower())


def rotulo(i):
    return str(playlist[i])


def sortear():
    st.session_state.musica_selecionada = random.choice(range(len(playlist)))


if "musica_selecionada" not in st.session_state:
    sortear()

# ---------------------------------------------------------------- Cabeçalho
st.title("🎵 Recomendador & Criador de Sequências (kNN)")
st.caption("Explore recomendações diretas ou crie uma transição continuada suave entre faixas.")

col_a, col_b = st.columns([8, 2])
with col_a:
    st.selectbox("Selecione a música inicial", ordem, format_func=rotulo, key="musica_selecionada")
with col_b:
    st.write("")
    st.write("")
    st.button("🎲 Sortear música", on_click=sortear, use_container_width=True)

musica_alvo = playlist[st.session_state.musica_selecionada]

# ---------------------------------------------------------------- Destaque da Música
st.divider()
st.subheader(f"📌 Música Base: {musica_alvo.nome}")
st.caption(f"Artista: **{musica_alvo.artista}**")

m1, m2, m3, m4 = st.columns(4)
m1.metric("💃 Dançabilidade", f"{musica_alvo.caracteristicas['danceability']:.2f}")
m2.metric("⚡ Energia", f"{musica_alvo.caracteristicas['energy']:.2f}")
m3.metric("😊 Valência", f"{musica_alvo.caracteristicas['valence']:.2f}")
m4.metric("🔊 Loudness", f"{musica_alvo.caracteristicas['loudness']:.2f}")

# ---------------------------------------------------------------- Configurações do Recomendador
st.divider()
col_modo, col_expoente, col_k = st.columns([4, 4, 3])

with col_modo:
    modo = st.radio(
        "Modo de Recomendação",
        ["Músicas Similares (Direto)", "Sequência Encadeada (Playlist Fluida)"],
        help="Direto mostra as mais parecidas com a base. Encadeada cria um caminho onde cada música se conecta à anterior.",
    )

with col_expoente:
    expoente_sel = st.radio(
        "Função de Custo",
        list(EXPOENTES),
        format_func=lambda e: EXPOENTES[e],
        help="O expoente 2 eleva a distância ao quadrado, suavizando saltos bruscos.",
    )

with col_k:
    k = st.slider("Quantidade de músicas", 1, 20, 5)

# ---------------------------------------------------------------- Resultados
if modo == "Músicas Similares (Direto)":
    st.subheader("🎧 Músicas mais parecidas")
    similares = knn.recomendar(musica_alvo, k=k, expoente=expoente_sel)

    dados = []
    for m, d in similares:
        sim_pct = max(0.0, min(100.0, (1 - d) * 100))
        dados.append({
            "Música": m.nome,
            "Artista": m.artista,
            "Similaridade": sim_pct / 100,
            "Distância": round(d, 4),
            "Energia": m.caracteristicas["energy"],
            "Dançabilidade": m.caracteristicas["danceability"],
        })

    st.dataframe(
        pd.DataFrame(dados),
        column_config={
            "Similaridade": st.column_config.ProgressColumn("Similaridade", format="%.1f%%", min_value=0, max_value=1),
            "Distância": st.column_config.NumberColumn("Distância Euclidiana", format="%.4f"),
        },
        hide_index=True,
        use_container_width=True,
    )

else:
    st.subheader("🔗 Sequência Encadeada de Transição Suave")
    sequencia_com_dist = knn.gerar_sequencia_suave(musica_alvo, tamanho=k, expoente=expoente_sel)

    # Prepara dados da tabela de sequência
    dados_seq = []
    for i, item in enumerate(sequencia_com_dist):
        if i == 0:
            m = item
            dist_passo = 0.0
        else:
            m, dist_passo = item

        dados_seq.append({
            "Ordem": i + 1,
            "Música": m.nome,
            "Artista": m.artista,
            "Salto (Distância)": round(dist_passo, 4),
            "Energia": round(m.caracteristicas["energy"], 2),
            "Valência": round(m.caracteristicas["valence"], 2),
        })

    df_seq = pd.DataFrame(dados_seq)
    st.dataframe(df_seq, hide_index=True, use_container_width=True)

    # Gráfico dos saltos ao longo da sequência
    if len(sequencia_com_dist) > 1:
        st.subheader("📈 Suavidade dos Saltos ao Longo da Playlist")
        st.caption("Quanto menor e mais constante o salto entre faixas vizinhas, mais suave é a transição.")
        saltos_df = pd.DataFrame({
            "Tamanho do Salto": [d for _, d in sequencia_com_dist[1:]]
        }, index=range(1, len(sequencia_com_dist)))
        st.line_chart(saltos_df)