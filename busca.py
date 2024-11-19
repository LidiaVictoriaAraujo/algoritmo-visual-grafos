from pyvis.network import Network
import networkx as nx
import time
from IPython.core.display import display, HTML, clear_output

import streamlit.components.v1 as components
import streamlit as st
import src.page as page
import tempfile


def create_visual_graph(graph, pos, path=None, visited_nodes=None, queue_nodes=None, final=False):
    net = Network(cdn_resources='in_line')
    # Configurações para exibir os labels corretamente
    net.set_options("""
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

    for node in graph.nodes():
        # Define as cores:
        # - Azul para o caminho final encontrado
        # - Laranja para os nós visitados que não fazem parte do caminho
        # - Amarelo para nós na fila (próximos)
        # - Cinza para nós não visitados
        if final:
            color = 'blue' if node in path else 'orange'
        else:
            if node in visited_nodes:
                color = 'blue'
            elif node in path:
                color = 'red'
            elif node in queue_nodes:
                color = 'purple'
            else:
                color = 'gray'

        # Define o nó com cor e posição fixa, escalando as coordenadas para evitar sobreposição
        x, y = pos[node]
        net.add_node(node, label=str(node), color=color, x=x * 1000, y=y * 1000, fixed=True)

    for edge in graph.edges():
        net.add_edge(*edge)

    text = net.generate_html('grafo_busca.html', local=True)

    with page.placeholder:
        page.placeholder.empty()
        components.html(text, height=600)

def bfs_visual(graph, pos, start, goal):
    visited = []  # Lista de nós já visitados
    queue = [[start]]  # Fila de caminhos a explorar, iniciando com o nó inicial

    while queue:
        path = queue.pop(0)  # Remove o primeiro caminho da fila
        node = path[-1]  # Último nó no caminho atual

        if node not in visited:
            visited.append(node)  # Marca o nó como visitado

            if node == goal:
                # Mostra o caminho final em azul e os nós restantes em laranja
                create_visual_graph(graph, pos, path=path, visited_nodes=visited, final=True)
                return path, visited  # Retorna o caminho e os nós visitados se o objetivo for encontrado
            
            new_path = None
            # Expande o nó atual para os vizinhos
            for neighbor in graph.neighbors(node):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)  # Adiciona o novo caminho à fila

            if new_path:

                queue_nodes = {n[-1] for n in queue if n[-1] not in visited}

                # Atualiza a visualização do grafo a cada passo
                create_visual_graph(graph, pos, path=new_path, visited_nodes=visited, queue_nodes=queue_nodes)
            else:
                return None, visited

            time.sleep(5)  # Pausa para ver a atualização da visualização

    return None, visited

def dfs_visual(graph, pos, start, goal):
    visited = set()  # Use um conjunto para rastrear os nós visitados
    stack = [(start, [start])]  # Pilha para armazenar nós e caminhos

    while stack:
        node, path = stack.pop()  # Remove o último nó e caminho da pilha

        if node not in visited:
            visited.add(node)  # Marca o nó como visitado

            if node == goal:
                # Mostra o caminho final em azul e os nós restantes em laranja
                create_visual_graph(graph, pos, path=path, visited_nodes=visited, final=True)
                return path, visited  # Retorna o caminho e os nós visitados se o objetivo for encontrado

            neighbors = list(graph.neighbors(node))
            for neighbor in reversed(neighbors):  # Visita os vizinhos em ordem inversa para simular uma pilha
                new_path = path + [neighbor]
                stack.append((neighbor, new_path))

            # Atualiza a visualização do grafo a cada passo
            create_visual_graph(graph, pos, path=path, visited_nodes=visited, queue_nodes={neighbor for neighbor in neighbors if neighbor not in visited})
            time.sleep(5) # Pausa para ver a atualização da visualização

    return None, visited  # Retorna None caso não encontre o caminho até o objetivo

def dijkstra_visual(graph, pos, start, goal):
    import heapq

    for edge in graph.edges():
        graph[edge[0]][edge[1]]['weight'] = 1  # Define peso 1 para todas as arestas

    # Dicionário para rastrear as distâncias mínimas
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start] = 0  # A distância inicial é zero

    # Fila de prioridade (min-heap)
    priority_queue = [(0, start)]  # Formato: (distância acumulada, nó)
    visited = []  # Nós visitados
    predecessors = {start: None}  # Para reconstruir o caminho

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.append(current_node)

        # Visualiza o estado atual do grafo
        create_visual_graph(graph, pos, path=visited, visited_nodes=visited, queue_nodes=[n for _, n in priority_queue])

        # Verifica se alcançamos o objetivo
        if current_node == goal:
            # Reconstrói o caminho
            path = []
            while current_node is not None:
                path.insert(0, current_node)
                current_node = predecessors[current_node]

            create_visual_graph(graph, pos, path=path, visited_nodes=visited, final=True)
            return path, visited

        # Examina os vizinhos
        for neighbor in graph.neighbors(current_node):
            edge_weight = graph[current_node][neighbor].get('weight', 1)  # Peso da aresta (padrão 1)
            new_distance = current_distance + edge_weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))
        time.sleep(5)  # Pausa para ver a atualização da visualização

    return None, visited  # Retorna None se não encontrar caminho