from pyvis.network import Network
import networkx as nx

HEIGHT = '500px'
WIDTH = '100%'

def make_grafo_aleatorio(v,a, dir):
    g = nx.gnm_random_graph(v, a, directed=dir)
    return g
    
def make_grafo_manual(v,a,ladj, dir):
    if dir:
        g=nx.DiGraph()
    else:
        g=nx.Graph()
    for i in range(v):
        g.add_node(i, label=i, title=str(i), labelHighlightBold=True)
    for i in range(v):
        for j in ladj[i]:
            g.add_edge(i,j)
    return g

def ler_html(g, dir):
    gvisual=Network(height=HEIGHT, width=WIDTH, directed=dir, notebook=False)
    gvisual.set_options("""
            var options = {
            "nodes": {
                "font": {
                "size": 32,
                "color": "#000000"
                },
                "scaling": {
                "label": true
                }
            }
            }
            """)
    gvisual.from_nx(g)
    gvisual.write_html('temp/grafo.html')
    HtmlFile = open("temp/grafo.html", 'r', encoding='utf-8')
    return HtmlFile.read()