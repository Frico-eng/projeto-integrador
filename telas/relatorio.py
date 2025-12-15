import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
caminho_projeto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, caminho_projeto)

from crud.crud_ingressos import listar_ingressos
print("Import realizado com sucesso!")

lista = listar_ingressos()
print(lista)