from src.page import page, modelagem, busca, mostra_componentes, caminho
import os
import streamlit as st

st.set_page_config(page_title='Trabalho de Grafos', page_icon='🧩', layout='wide', initial_sidebar_state='expanded')


inicializacao = ['v', 'a', 'grafo', 'direcionado']
for i in inicializacao:
    if i not in st.session_state:
        st.session_state[i] = None
os.makedirs('temp', exist_ok=True)

st.sidebar.subheader('Informações do grafo')
st.sidebar.write("Aqui nós temos as principais informações sobre o seu grafo. Você pode gerar um grafo aleatório ou inserir manualmente as arestas.")
st.sidebar.write("Número de vértices: ", st.session_state.v)
st.sidebar.write("Número de arestas: ", st.session_state.a)
# st.sidebar.write("Direcionado: ", st.session_state.direcionado)

pages = st.sidebar.radio('Selecione a página', ['Página Inicial', 'Modelagem do Grafo', 'Busca de vértices', 'Caminho mínimo', 'Cálculo de componentes'])

if pages == 'Página Inicial':
    page()
elif pages == 'Modelagem do Grafo':
    modelagem()
elif pages == 'Busca de vértices':
    busca()
elif pages == 'Caminho mínimo':
    caminho()
elif pages == 'Cálculo de componentes':
    mostra_componentes()
else:
    st.write("Selecione uma página no menu lateral")

with open('docs/Documentação - Algoritmos em grafos.pdf', 'rb') as file:
    st.sidebar.download_button('Clique aqui para baixar a documentação do projeto', 
                               data=file, 
                               file_name='Documentação - Algoritmo em grafos.pdf')
    
with open('docs/metodologia.html', 'r', encoding='utf-8') as f:
        st.sidebar.html(f.read())
