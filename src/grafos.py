from pyvis.network import Network
import networkx as nx

HEIGHT = '500px'
WIDTH = '100%'

def make_grafo_aleatorio(v,a, dir):
    g=Network(height=HEIGHT, width=WIDTH, directed=dir, notebook=False)
    g.barnes_hut()
    g.from_nx(nx.gnm_random_graph(v, a))
    return g
    
def make_grafo_manual(v,a,ladj, dir):
    g=Network(height=HEIGHT, width=WIDTH, directed=dir, notebook=False)
    g.barnes_hut()
    for i in range(v):
        g.add_node(i, label=i, title=str(i), labelHighlightBold=True)
    for i in range(v):
        for j in ladj[i]:
            g.add_edge(i,j)
    return g

def ler_html(g):
    g.write_html('temp/grafo.html')
    HtmlFile = open("temp/grafo.html", 'r', encoding='utf-8')
    return HtmlFile.read()