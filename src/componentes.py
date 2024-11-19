from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components

colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 'black', 'gray', 'cyan', 'magenta', 'olive', 'navy', 'lime', 'teal', 'aqua', 'maroon', 'fuchsia', 'silver', 'white']

def visitaDFS(adj, u, d, f, cor, tempo):
    saidaTexto = "(%d " % u
    tempo[0] += 1
    d[u] = tempo[0]
    cor[u] = 1
    for v in adj[u]:
        if cor[v] == 0:
            saidaTexto += visitaDFS (adj, v, d, f, cor, tempo)

    saidaTexto += "%d) " % u
    tempo[0] += 1
    f[u] = tempo[0]
    cor[u] = 2
    return saidaTexto

def DFS(adj, verticesOrdenados):
    n = len(adj)
    cor = [0] * n
    d = [0] * n
    f = [0] * n
    for u in range(n):
        cor[u] = 0
    tempo = [0]
    saidaTexto = ""
    for u in verticesOrdenados:
        if cor[u] == 0:
            saidaTexto += visitaDFS (adj, u, d, f, cor, tempo)
    return f, saidaTexto

def matriz_transposta(adj):
    n = len(adj)
    adjT = [[] for _ in range(n)]
    for i in range(n):
        for j in adj[i]:
            adjT[j].append(i)
    return adjT

def duplicar_lista_ate_tamanho(lista, tamanho):
    if not lista:
        return lista

    while len(lista) < tamanho:
        lista += lista

    return lista[:tamanho]  # Retorna a lista cortada ao tamanho desejado

def transforma_componentes(f, saidaTexto, grafo, pos):
    net = Network(cdn_resources='in_line')
    groups = []
    saidaTexto = saidaTexto.replace("(", "")
    saidaTexto = saidaTexto.replace(")", "")
    vertices = saidaTexto.split(" ")
    add = []
    i = 0
    while True:
        elem = vertices[i]
        if elem == "":
            break
        elif elem not in add:
            add.append(elem)
            fim = vertices[i+1:].index(elem)
            new_group = vertices[i:(i+fim+1)]
            groups.append(list(set(new_group)))
            i = i+fim+1
        else:
            i+=1
            pass

    n_componentes = len(groups)
    if len(groups) > len(colors):
        colors_list = duplicar_lista_ate_tamanho(colors, n_componentes)
    else:
        colors_list = colors[:n_componentes]
    for i in range(n_componentes):
        for v in groups[i]:
            a = int(v)
            net.add_node(a, label=v, color=colors_list[i], x=pos[a][0]*1000, y=pos[a][1]*1000, fixed=True)

    for edge in grafo.edges():
        net.add_edge(*edge)

    text = net.generate_html('grafo_componentes.html', local=True)
    components.html(text, height=600)
    return n_componentes

def componentes(grafo, pos):
    edges = grafo.edges()
    adj = [[] for _ in range(grafo.number_of_nodes())]
    for edge in edges:
        adj[edge[0]].append(edge[1])
    adjT = matriz_transposta(adj)
    f, saidaTexto = DFS(adj, range(len(adj)))
    verticesOrdenados = sorted(range(len(f)), key=lambda x: f[x], reverse=True)
    f, saidaTexto = DFS(adjT, verticesOrdenados)
    n_componentes = transforma_componentes(f, saidaTexto, grafo, pos)
    return saidaTexto, n_componentes