import json
import re

import networkx as nx
from pyvis.network import Network

COR_CAMINHO = "#e63946"
COR_ORIGEM = "#2a9d8f"
COR_DESTINO = "#1d6fd8"
COR_CONTEXTO = "#9aa5b1"

ESCALA_POSICAO = 450       # leva o layout inicial (-1..1) para pixels
COMPRIMENTO_BASE = 60      # tamanho "de repouso" mínimo de cada mola (aresta)
COMPRIMENTO_POR_PESO = 350 # quanto o peso alonga a mola: mais distantes, mais longe

# Configuração do vis-network (a biblioteca que faz a física no navegador)
OPCOES = {
    "physics": {
        "enabled": True,
        "solver": "forceAtlas2Based",
        "forceAtlas2Based": {
            "gravitationalConstant": -70,  # nós se repelem...
            "springConstant": 0.08,        # ...e as arestas puxam como molas
            "centralGravity": 0.01,
            "damping": 0.45,
            "avoidOverlap": 0.6,
        },
        "stabilization": {"enabled": True, "iterations": 250, "updateInterval": 25},
    },
    "interaction": {
        "hover": True,
        "dragNodes": True,
        "dragView": True,
        "zoomView": True,
        "tooltipDelay": 80,
    },
    "nodes": {
        "shape": "dot",
        "borderWidth": 2,
        "font": {"size": 16, "color": "#222222", "strokeWidth": 4, "strokeColor": "#ffffff"},
    },
    "edges": {
        "smooth": False,
        "font": {"size": 12, "strokeWidth": 4, "strokeColor": "#ffffff", "align": "horizontal"},
    },
}


def montar_subgrafo(grafo, caminho, max_vizinhos):
    """
    Recorta só a região do grafo que importa para o desenho:
      - nós: as músicas do caminho + as `max_vizinhos` vizinhas mais
        próximas de cada uma delas (contexto);
      - arestas: todas as que encostam em alguma música do caminho.
    Desenhar o grafo inteiro (centenas de nós e milhares de arestas)
    viraria um emaranhado ilegível.
    """
    nos = set(caminho)
    for musica in caminho:
        mais_proximos = sorted(grafo.obter_vizinhos(musica).items(), key=lambda item: item[1])
        nos.update(vizinho for vizinho, _ in mais_proximos[:max_vizinhos])

    sub = nx.Graph()
    sub.add_nodes_from(nos)
    for musica in caminho:
        for vizinho, peso in grafo.obter_vizinhos(musica).items():
            if vizinho in nos:
                # afinidade = 1/peso: quanto mais parecidas, mais o layout as aproxima
                sub.add_edge(musica, vizinho, peso=peso, afinidade=1 / max(peso, 1e-6))
    return sub


def _cor_do_no_do_caminho(posicao, total):
    if posicao == 0:
        return COR_ORIGEM
    if posicao == total - 1:
        return COR_DESTINO
    return COR_CAMINHO


def montar_html(sub, caminho, posicoes, mostrar_pesos_contexto=False, altura=720):
    rede = Network(
        height=f"{altura}px",
        width="100%",
        bgcolor="#ffffff",
        font_color="#222222",
        cdn_resources="in_line",  # embute o vis-network: não depende de internet
    )
    rede.set_options(json.dumps(OPCOES))

    ordem_no_caminho = {musica: i for i, musica in enumerate(caminho)}

    for musica in sub.nodes:
        x, y = posicoes[musica]
        # o layout inicial só dá a posição de partida; depois a física assume
        base = dict(x=float(x) * ESCALA_POSICAO, y=float(y) * ESCALA_POSICAO,
                    title=f"{musica.nome}\n{musica.artista}")

        if musica in ordem_no_caminho:
            i = ordem_no_caminho[musica]
            rede.add_node(
                musica.id,
                label=f"{i + 1}. {musica.nome[:26]}",
                color=_cor_do_no_do_caminho(i, len(caminho)),
                size=24,
                **base,
            )
        else:
            rede.add_node(musica.id, label=" ", color=COR_CONTEXTO, size=10, **base)

    pares_do_caminho = {frozenset(par) for par in zip(caminho, caminho[1:])}

    for a, b, dados in sub.edges(data=True):
        peso = dados["peso"]
        no_caminho = frozenset((a, b)) in pares_do_caminho
        opcoes_aresta = dict(
            title=f"Peso: {peso:.4f}",
            # comprimento de repouso da mola: quanto maior o peso, mais afastados
            length=COMPRIMENTO_BASE + COMPRIMENTO_POR_PESO * peso,
            color=COR_CAMINHO if no_caminho else COR_CONTEXTO,
            width=4 if no_caminho else 1,
        )
        if no_caminho or mostrar_pesos_contexto:
            opcoes_aresta["label"] = f"{peso:.3f}"
            opcoes_aresta["font"] = {
                "size": 15 if no_caminho else 11,
                "color": COR_CAMINHO if no_caminho else "#6b7480",
                "strokeWidth": 4,
                "strokeColor": "#ffffff",
                "align": "horizontal",
            }
        rede.add_edge(a.id, b.id, **opcoes_aresta)

    html = rede.generate_html(notebook=False)

    # o pyvis puxa o bootstrap da internet só para estilizar a borda; troca por CSS próprio
    html = re.sub(r"<link[^>]*bootstrap[^>]*>", "", html)
    html = re.sub(r"<script[^>]*bootstrap[^>]*></script>", "", html)
    estilo = "<style>body{margin:0}#mynetwork{border:1px solid #d0d5db;border-radius:6px}</style>"
    return html.replace("</head>", estilo + "</head>", 1)


def html_do_caminho(grafo, caminho, max_vizinhos=6, mostrar_pesos_contexto=False, altura=720):
    """Devolve (html, subgrafo): o desenho com física e o recorte usado nele."""
    sub = montar_subgrafo(grafo, caminho, max_vizinhos)
    # seed fixa: o mesmo recorte sempre parte das mesmas posições
    posicoes = nx.spring_layout(sub, weight="afinidade", seed=42, iterations=100)
    return montar_html(sub, caminho, posicoes, mostrar_pesos_contexto, altura), sub