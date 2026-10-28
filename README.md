# 🎵 Projeto IA: Busca em Grafo para Gerar Sequências de Músicas

Uma aplicação em Python para a geração de playlists e transições musicais contínuas. O sistema utiliza **busca em grafos (algoritmo de Dijkstra)** e **kNN (*k-Nearest Neighbors*)** para encontrar caminhos entre duas músicas, buscando tornar as transições entre faixas suaves, graduais e musicalmente coerentes.

---

## Motivação e Objetivo

Escolher sequências de músicas aleatórias ou baseadas apenas no gênero pode resultar em diferenças significativas de ritmo, harmonia e outras características sonoras entre faixas consecutivas. Para reduzir essas diferenças, o projeto representa as músicas em um **grafo de similaridade sonora**, no qual os nós correspondem às faixas e as arestas representam conexões entre músicas com características sonoras semelhantes.

A partir de uma música inicial e outra de destino, a aplicação utiliza o algoritmo de Dijkstra para encontrar um caminho entre elas, considerando os custos das transições entre faixas. Dessa forma, busca-se selecionar músicas intermediárias que tornem a progressão das características sonoras mais gradual, proporcionando uma transição mais fluida para o ouvinte.

---

## Recursos Principais

- **Normalização de Atributos de Áudio:** considera parâmetros acústicos como *danceability*, *energy*, *valence*, *tempo*, *acousticness*, *instrumentalness*, *loudness*, *speechiness* e *liveness*.
- **Grafo de Similaridade Musical:** representa as músicas como nós e as conexões entre elas como arestas, de acordo com a proximidade sonora.
- **Suavização de Saltos (Dijkstra):** utiliza um algoritmo de menor caminho com expoentes configuráveis para penalizar transições com diferenças sonoras maiores.
- **Recomendação kNN:** identifica faixas semelhantes à música de referência.
- **Interface Interativa:** oferece um painel web para seleção de músicas, simulação de rotas e visualização gráfica dos resultados.

---

## Tech Stack

- **Linguagem:** Python 3.9+
- **Interface Web:** [Streamlit](https://streamlit.io/)
- **Processamento de Dados:** Pandas e NumPy
- **Estruturas e Algoritmos:** `heapq` (fila de prioridade), `pickle` (serialização e cache local), `math`, `re` e `pathlib`.
- **Armazenamento:** arquivo local `data/playlist.csv` e cache em `data/grafo_cache.pkl`.

---

## Dataset

O conjunto de dados utilizado neste projeto foi obtido a partir de uma playlist do Spotify pertencente a um dos integrantes da equipe. Os dados são armazenados localmente no arquivo `data/playlist.csv` e utilizados tanto na geração de rotas musicais quanto na recomendação de faixas semelhantes.

---

## Estrutura do Projeto

```text
projeto-ia-musicas/
├── data/
│   ├── playlist.csv        # Dataset com as faixas e os atributos de áudio
│   └── grafo_cache.pkl     # Cache do grafo, gerado automaticamente
├── app.py                  # Interface web interativa com Streamlit
├── main.py                 # Execução no terminal e análises
├── grafo.py                # Estrutura do grafo e implementação do Dijkstra
├── musica.py               # Classe Musica e cálculo de distância euclidiana
├── gerar_grafo.py          # Processamento do CSV e construção do grafo
├── recomendador_knn.py     # Recomendação por vizinhos mais próximos
├── .gitignore              # Configuração de arquivos ignorados pelo Git
└── README.md               # Documentação do projeto
```

---

## Como Executar o Projeto

#### 1. Pré-requisitos

Certifique-se de ter o **Python 3.9 ou superior** e o **pip** instalados em sua máquina.

#### 2. Clonar o Repositório

```bash
git clone https://github.com/lucasfariasbl/projeto-ia-musicas.git
cd projeto-ia-musicas
```

#### 3. Criar e Ativar o Ambiente Virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 4. Instalar as Dependências

```bash
python -m pip install --upgrade pip
pip install numpy pandas streamlit
```

---

## Uso da Aplicação

#### Opção A: Execução via Terminal (Análise e Testes)

Executa a lógica de carregamento do grafo, cálculo de componentes conexos e comparação de caminhos.

```bash
python main.py
```

#### Opção B: Interface Web Interativa (Streamlit)

Inicia o painel gráfico no navegador para explorar as rotas musicais e as recomendações.

```bash
streamlit run app.py
```

## Funcionalidades da Interface

1. **Seleção de Músicas:** escolha a música de origem e a de destino ou sorteie um par aleatório.
2. **Caminho Otimizado:** visualize a lista de músicas intermediárias sugeridas pelo Dijkstra.
3. **Métricas de Transição:** analise o maior salto e o salto médio entre as faixas da rota.
4. **Gráficos de Perfil:** acompanhe a variação das características sonoras ao longo do percurso.
5. **Recomendações kNN:** consulte as faixas mais semelhantes a qualquer música selecionada.

---

## Fundamentos Algorítmicos

- **Cálculo de Distância:** utiliza a distância euclidiana ponderada entre os vetores de atributos sonoros normalizados para estimar a similaridade entre as músicas.
- **Construção do Grafo:** as músicas são representadas por nós, enquanto as arestas conectam faixas consideradas semelhantes, com custos definidos a partir das diferenças entre seus atributos sonoros.
- **Busca de Menor Caminho (Dijkstra):** encontra o caminho de menor custo entre a música inicial e a música de destino, considerando os pesos das arestas do grafo.
  - `expoente = 1`: utiliza as distâncias como custos das transições, minimizando a soma dos custos ao longo do caminho.
  - `expoente = 2`: eleva as distâncias ao quadrado, penalizando mais intensamente as transições com diferenças sonoras maiores.
- **Limitação da Abordagem:** a penalização de saltos maiores pode favorecer uma progressão sonora mais gradual, mas não garante uma transição musicalmente perfeita. O resultado depende das conexões disponíveis no grafo e da distribuição das características sonoras das faixas.
- **Sistema de Cache:** o grafo é salvo localmente em `data/grafo_cache.pkl` após sua construção, permitindo reutilizá-lo em execuções posteriores.

---

## Equipe e Informações do Projeto

- **Integrantes:**
  - Fabiana Simplicio da Silva
  - Gabriel Paulo Ribeiro
  - Gustavo Miguel de Lima Anisio
  - Lucas Farias Bezerra de Lima
  - Pedro Leal e Lima
- **Componente Curricular:** Inteligência Artificial
- **Professor:** Eanes Torres Pereira
- **Período:** 2026.5

---

**Observação:** Este projeto foi desenvolvido para fins educacionais, com foco no estudo de Inteligência Artificial e Algoritmos de Busca.