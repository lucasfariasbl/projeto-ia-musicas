# 🎵 Projeto IA: Recomendador & Criador de Playlists Fluidas com kNN

Uma aplicação em Python para recomendação de músicas e geração de sequências sonoras contínuas. O sistema utiliza o algoritmo **kNN (*k-Nearest Neighbors*)** combinado com **funções de penalização de distância configuráveis (expoentes)** para encontrar faixas semelhantes e criar playlists com transições suaves, graduais e musicalmente coerentes.

---

## Motivação e Objetivo

Escolher sequências de músicas aleatórias ou baseadas apenas no gênero pode resultar em mudanças bruscas de ritmo, harmonia e energia entre faixas consecutivas. Para evitar esse choque acústico, o projeto representa as músicas através de vetores de características sonoras normalizadas e calcula a proximidade entre elas no espaço de atributos.

A partir de uma música inicial, a aplicação permite duas abordagens:
1. **Recomendação Direta:** identifica as faixas mais parecidas com a música base.
2. **Sequência Encadeada (Playlist Fluida):** gera uma fila de reprodução onde cada nova faixa é selecionada com base na música imediatamente anterior, criando um fluxo sonoro contínuo ("efeito DJ").

O sistema também oferece uma **função de custo com expoente quadrático (expoente 2)**, que penaliza desvios grandes em atributos individuais (como saltos repentinos de BPM ou Energia), garantindo que a transição entre músicas consecutivas ocorra de forma extremamente suave.

---

## Recursos Principais

- **Normalização de Atributos de Áudio:** considera parâmetros acústicos como *danceability*, *energy*, *valence*, *tempo*, *acousticness*, *instrumentalness*, *loudness*, *speechiness* e *liveness*.
- **Recomendação kNN Direta:** encontra as $k$ músicas mais próximas de uma faixa de referência.
- **Sequência Encadeada (Playlist Fluida):** gera uma transição continuada "passo a passo" usando kNN iterativo.
- **Suavização Ponderada de Transições (Expoente 1 vs 2):**
  - **Expoente 1 (Linear):** permite saltos maiores em características isoladas, gerando transições mais dinâmicas.
  - **Expoente 2 (Quadrático):** penaliza fortemente qualquer variação brusca de atributo, forçando uma transição contínua e suave.
- **Interface Web Interativa:** painel em Streamlit com métricas visuais da música base, barras de similaridade %, tabelas configuráveis e gráficos de linha para acompanhar a suavidade dos saltos.

---

## Tech Stack

- **Linguagem:** Python 3.9+
- **Interface Web:** [Streamlit](https://streamlit.io/)
- **Processamento de Dados:** Pandas e NumPy
- **Estruturas e Algoritmos:** `heapq` (fila de prioridade), `pickle` (serialização e cache local), `math`, `re` e `pathlib`.
- **Armazenamento:** arquivo local `data/playlist.csv` e cache em `data/grafo_cache.pkl`.

---

## Dataset

O conjunto de dados utilizado neste projeto foi obtido a partir de uma playlist do Spotify pertencente a um dos integrantes da equipe. Os dados são armazenados localmente no arquivo `data/playlist.csv` e utilizados para alimentar os cálculos de distância vetorial e recomendação.

---

## Estrutura do Projeto

```text
projeto-ia-musicas/
├── data/
│   ├── playlist.csv         # Dataset com as faixas e os atributos de áudio
│   └── grafo_cache.pkl      # Cache serializado do dataset e estruturas
├── app.py                   # Interface web interativa com Streamlit
├── main.py                  # Script para testes CLI e verificação do cache
├── grafo.py                 # Estrutura de dados para armazenamento do conjunto
├── musica.py                # Classe Musica e cálculo de distância ponderada (Expoentes 1 e 2)
├── gerar_grafo.py           # Leitura, tratamento do CSV e estruturação dos dados
├── recomendador_knn.py      # Recomendação kNN e geração de sequências encadeadas
├── .gitignore               # Configuração de arquivos ignorados pelo Git
└── README.md                # Documentação do projeto