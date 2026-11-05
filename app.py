import random

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from main import carregar_grafo
from recomendador_knn import RecomendadorKNN
from visualizar import html_do_caminho

st.set_page_config(page_title="Recomendador de Músicas", layout="wide")


@st.cache_resource(show_spinner="Carregando dados...")
def carregar():
    grafo, playlist = carregar_grafo()
    return grafo, playlist, RecomendadorKNN(playlist)


try:
    grafo, playlist, knn = carregar()
except Exception as erro:
    st.error(f"Não foi possível carregar os dados: {erro}")
    st.stop()

# opções do seletor: índices da playlist em ordem alfabética
ordem = sorted(range(len(playlist)), key=lambda i: str(playlist[i]).lower())


def rotulo(i):
    return str(playlist[i])


def mostrar_html(html, altura):
    # st.iframe existe nas versões novas do Streamlit; components.html, nas antigas
    if hasattr(st, "iframe"):
        st.iframe(html, height=altura)
    else:
        components.html(html, height=altura)


def sortear():
    st.session_state.musica_selecionada = random.choice(range(len(playlist)))


if "musica_selecionada" not in st.session_state:
    sortear()

# ---------------------------------------------------------------- Cabeçalho
st.title("🎵 Recomendador de Músicas Similares (kNN)")
st.caption("Selecione uma música e descubra faixas com perfil sonoro equivalente com base em características de áudio.")

col_a, col_b = st.columns([8, 2])
with col_a:
    st.selectbox("Selecione uma música base", ordem, format_func=rotulo, key="musica_selecionada")
with col_b:
    st.write("")
    st.write("")
    st.button("🎲 Sortear música", on_click=sortear, use_container_width=True)

musica_alvo = playlist[st.session_state.musica_selecionada]

# ---------------------------------------------------------------- Destaque da Música Alvo
st.divider()
st.subheader(f"📌 Música Selecionada: {musica_alvo.nome}")
st.caption(f"Artista: **{musica_alvo.artista}**")

# Exibe os principais atributos em métricas visuais
m1, m2, m3, m4 = st.columns(4)
m1.metric("💃 Dançabilidade", f"{musica_alvo.caracteristicas['danceability']:.2f}")
m2.metric("⚡ Energia", f"{musica_alvo.caracteristicas['energy']:.2f}")
m3.metric("😊 Valência (Humor)", f"{musica_alvo.caracteristicas['valence']:.2f}")
m4.metric("🔊 Loudness", f"{musica_alvo.caracteristicas['loudness']:.2f}")

# ---------------------------------------------------------------- Seção do kNN
st.divider()
col_titulo, col_slider = st.columns([6, 4])
with col_titulo:
    st.subheader("🎧 Músicas Recomendadas")
with col_slider:
    k = st.slider("Quantidade de recomendações (k)", 1, 20, 5)

similares = knn.recomendar(musica_alvo, k)

# Monta o DataFrame com mais dados e formatação amigável
dados_tabela = []
for m, d in similares:
    # Transforma distância matemática em porcentagem de similaridade simples
    sim_pct = max(0.0, min(100.0, (1 - d) * 100))
    dados_tabela.append({
        "Música": m.nome,
        "Artista": m.artista,
        "Similaridade": sim_pct / 100,  # O Streamlit formata decimal em %
        "Distância": round(d, 4),
        "Energia": m.caracteristicas["energy"],
        "Dançabilidade": m.caracteristicas["danceability"],
    })

df_similares = pd.DataFrame(dados_tabela)

# Tabela estilizada com bar progressivo para similaridade
st.dataframe(
    df_similares,
    column_config={
        "Similaridade": st.column_config.ProgressColumn(
            "Similaridade",
            help="Grau de semelhança sonora com a música base",
            format="%.1f%%",
            min_value=0,
            max_value=1,
        ),
        "Distância": st.column_config.NumberColumn("Distância Euclidiana", format="%.4f"),
        "Energia": st.column_config.NumberColumn("Energia", format="%.2f"),
        "Dançabilidade": st.column_config.NumberColumn("Dançabilidade", format="%.2f"),
    },
    hide_index=True,
    use_container_width=True,
)

# ---------------------------------------------------------------- Comparativo Visual
if similares:
    st.subheader("📊 Comparativo da 1ª Recomendação vs. Música Base")
    top_1, _ = similares[0]

    df_comp = pd.DataFrame({
        "Atributo": list(musica_alvo.caracteristicas.keys()),
        musica_alvo.nome: list(musica_alvo.caracteristicas.values()),
        top_1.nome: list(top_1.caracteristicas.values()),
    }).set_index("Atributo")
