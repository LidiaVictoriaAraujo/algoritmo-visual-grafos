from pyvis.network import Network
import networkx as nx

HEIGHT = '500px'
WIDTH = '100%'

def make_grafo_aleatorio(v,a, dir):
    g = nx.gnm_random_graph(v, a)
    return g
    
def make_grafo_manual(v,a,ladj, dir):
    g=nx.Graph()
    for i in range(v):
        g.add_node(i, label=i, title=str(i), labelHighlightBold=True)
    for i in range(v):
        for j in ladj[i]:
            g.add_edge(i,j)
    return g

def ler_html(g):
    gvisual=Network(height=HEIGHT, width=WIDTH, notebook=False)
    gvisual.from_nx(g)
    gvisual.write_html('temp/grafo.html')
    HtmlFile = open("temp/grafo.html", 'r', encoding='utf-8')
    return HtmlFile.read()