import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import networkx as nx

from src.grafos import make_grafo_aleatorio, make_grafo_manual, ler_html
from src.busca import bfs_visual, dfs_visual, dijkstra_visual
from src.componentes import componentes

class Busca:
        def __init__(self) -> None:
            self.inicio = None
            self.final = None
            self.image_final = None
            pass

def page():
    st.title('Trabalho final da disciplina de Algoritmos em Grafos')
    st.write('Este é o trabalho de Grafos da disciplina de Algoritmos em Grafos. O algoritmo é implementado em Python e a interface gráfica é feita com o Streamlit.')

    st.divider()

    with open('docs/intro.html', 'r', encoding='utf-8') as f:
        st.html(f.read())



def modelagem():
    st.header('Modelagem do grafo')

    colv, cola = st.columns([1, 1])
    
    with colv:
        st.subheader('Grafo Aleatório')
        v = st.number_input(label='digite o número de vértices',step=1, key='vrand')
        a = st.number_input(label='digite o número de arestas', step=1, key='arand')
        dir = st.toggle('Grafo direcionado', key='dirrand', value=True)
        aleatorio = st.button('Gera Grafo Aleatório', use_container_width=True)
        if aleatorio:
            st.session_state.v = v
            st.session_state.a = a
            st.session_state.direcionado = dir
            st.session_state.grafo = make_grafo_aleatorio(st.session_state.v, st.session_state.a, dir)

    with cola:
        st.subheader('Grafo  Definido')
        v = st.number_input(label='digite o número de vértices',step=1, key='vman')
        text_arestas = st.text_area("Digite as combinações de arestas no formato 'vértice aresta'")
        dir = st.toggle('Grafo direcionado', key='dirmand', value=True)
        gera = st.button("Gerar Grafo", use_container_width=True)
        if gera:
            arestas = text_arestas.split('\n')
            st.session_state.v = v
            st.session_state.a = len(arestas)
            st.session_state.direcionado = dir
            ladj = [[] for _ in range(v)]
            for aresta in arestas:
                v, a = aresta.split(' ')
                ladj[int(v)].append(int(a))
            st.session_state.grafo = make_grafo_manual(st.session_state.v, st.session_state.a, ladj, dir)

    #colocar divisória
    st.markdown('---')
    if st.session_state.grafo:
        components.html(ler_html(st.session_state.grafo, dir=st.session_state.direcionado), height=600)
    else:
        st.write('Ainda não foi gerado um grafo')

def busca():
    st.header('Buscar vértice no Grafo')
    st.write('Aqui você pode buscar um vértice no grafo gerado anteriormente. Digite o vértice que deseja buscar, o vértice inicial e selecione o tipo de busca que gostaria de fazer e clique em buscar.')

    if not st.session_state.grafo:
        st.write('Gere um grafo antes de buscar um vértice. É possível gerar um grafo na opção Modelagem do Grafo no menu lateral.')
    else:
        busca = Busca()
        colin, colbusca = st.columns([1, 1])
        with colin:
            inicio = st.number_input(label='Digite o vértice inicial', step=1, key='inicio')
            busca.inicio = inicio
        with colbusca:
            fim = st.number_input(label='Digite o vértice que deseja buscar', step=1, key='busca')
            busca.final = fim
        tipo = st.selectbox('Selecione o tipo de busca', ['Busca em Largura', 'Busca em Profundidade'])

        if tipo == 'Busca em Largura':
            with open('docs/bfs_resumido.html', 'r', encoding='utf-8') as f:
                st.html(f.read())
        else:
            with open('docs/dfs_resumido.html', 'r', encoding='utf-8') as f:
                st.html(f.read())

        if st.button('Buscar', use_container_width=True):
            if busca.inicio < 0 or busca.inicio >= st.session_state.v:
                st.write('Vértice inválido. Digite um vértice entre 0 e ', str(st.session_state.v-1))
            elif busca.final < 0 or busca.final >= st.session_state.v:
                st.write('Vértice inválido. Digite um vértice entre 0 e ', str(st.session_state.v-1))
            else:
                if tipo == 'Busca em Largura':
                    pos = nx.spring_layout(st.session_state.grafo, seed=42)
                    path, visited_nodes = bfs_visual(st.session_state.grafo, pos, busca.inicio, busca.final)
                else:
                    pos = nx.spring_layout(st.session_state.grafo, seed=42)
                    path, visited_nodes = dfs_visual(st.session_state.grafo, pos, busca.inicio, busca.final)
                if path:
                    string=' -> '.join([str(node) for node in path])
                    st.subheader(f'Caminho encontrado: {string}')
                else:
                    st.subheader('Caminho não encontrado')

def mostra_componentes():
    st.header('Cáclulo dos componentes fortemente conexos do Grafo')
    st.write('Aqui você pode calcular os componentes fortemente conexos do grafo gerado anteriormente. Clique no botão abaixo para calcular os componentes.')
    st.divider()
    gerar = st.button('Calcular componentes', use_container_width=True)
    if gerar:
        if not st.session_state.grafo:
            st.write('Gere um grafo antes de encontrar os componentes. É possível gerar um grafo na opção Modelagem do Grafo no menu lateral.')
        else:
            pos = nx.spring_layout(st.session_state.grafo, seed=42)
            saidatexto, n_componentes = componentes(grafo=st.session_state.grafo, pos=pos)
            st.subheader(f'Este grafo contém {n_componentes} componentes')
            st.subheader(f'Sua representação por parênteses é dada por \n {saidatexto}')

def caminho():
    st.header('Caminho mínimo no Grafo')
    st.write('Aqui você pode buscar o caminho mínimo entre dois vértices no grafo gerado anteriormente. Digite o vértice inicial e final e clique em buscar.')
    if not st.session_state.grafo:
        st.write('Gere um grafo antes de buscar um caminho. É possível gerar um grafo na opção Modelagem do Grafo no menu lateral.')
    else:
        busca = Busca()
        colin, colbusca = st.columns([1, 1])
        with colin:
            inicio = st.number_input(label='Digite o vértice inicial', step=1, key='inicio')
            busca.inicio = inicio
        with colbusca:
            fim = st.number_input(label='Digite o vértice que deseja buscar', step=1, key='busca')
            busca.final = fim
        if st.button('Buscar', use_container_width=True):
            if busca.inicio < 0 or busca.inicio >= st.session_state.v:
                st.write('Vértice inválido. Digite um vértice entre 0 e ', str(st.session_state.v-1))
            elif busca.final < 0 or busca.final >= st.session_state.v:
                st.write('Vértice inválido. Digite um vértice entre 0 e ', str(st.session_state.v-1))
            else:
                st.write('Buscando caminho mínimo entre os vértices', inicio, 'e', fim)
                pos = nx.spring_layout(st.session_state.grafo, seed=42)
                path, visited_nodes = dijkstra_visual(st.session_state.grafo, pos, busca.inicio, busca.final)
                if path:
                    string=' -> '.join([str(node) for node in path])
                    st.subheader(f'Caminho mínimo encontrado: {string}')
                else:
                    st.subheader('Caminho mínimo não encontrado')
