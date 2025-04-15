# main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from collections import deque
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from fastapi.responses import JSONResponse


app = FastAPI()

# Permitir chamadas do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregar o dataset
df = pd.read_parquet("taco-db-nutrientes.parquet")
nutrientes = ['Proteína (g)', 'Lipídeos (g)', 'Carboidrato (g)', 'Fibra Alimentar (g)', 'Cálcio (mg)']

for col in nutrientes:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Função de distância
def calcular_similaridade(a1, a2):
    return sum(abs(a1[n] - a2[n]) for n in nutrientes)

# Construir grafo
grafo = {}
for i, a1 in df.iterrows():
    nome1 = a1['Nome']
    grafo[nome1] = []
    for j, a2 in df.iterrows():
        if i != j:
            nome2 = a2['Nome']
            distancia = calcular_similaridade(a1, a2)
            informacao = []
            grafo[nome1].append((nome2, distancia))

def substitutos_bfs(inicio, max_resultados=5):
    if inicio not in grafo:
        return []

    visitados = set()
    fila = deque([inicio])
    substitutos = []

    # Buscar o alimento inicial no dataset
    alimento_info = df[df['Nome'] == inicio][['Nome'] + nutrientes]
    if alimento_info.empty:
        return {"erro": "Alimento inicial não encontrado no dataset"}
    
    alimento_info = alimento_info.to_dict(orient="records")[0]

    while fila and len(substitutos) < max_resultados:
        atual = fila.popleft()
        if atual not in visitados:
            visitados.add(atual)
            vizinhos_ordenados = sorted(grafo[atual], key=lambda x: x[1])

            for vizinho, dist in vizinhos_ordenados:
                if vizinho not in visitados:
                    fila.append(vizinho)

                    # Obter as informações nutricionais do vizinho
                    substituto_info = df[df['Nome'] == vizinho][['Nome'] + nutrientes]
                    if not substituto_info.empty:
                        substituto_info = substituto_info.to_dict(orient="records")[0]
                        substitutos.append({
                            "nome": vizinho,
                            "distancia": dist,
                            "informacoes_nutricionais": substituto_info
                        })

                    if len(substitutos) >= max_resultados:
                        break
    print({"alimento_inicial": alimento_info, "substitutos": substitutos})
    return {"alimento_inicial": alimento_info, "substitutos": substitutos}


@app.get("/search")
def buscar_alimentos(q: str = Query("")):
    resultados = df[df['Nome'].str.contains(q, case=False, na=False)]['Nome'].unique().tolist()
    return resultados



@app.get("/substitutes")
def obter_substitutos(alimento: str):
    resultado = substitutos_bfs(alimento)
    if 'erro' in resultado:
        return JSONResponse(status_code=400, content=resultado)
    return resultado


# Servir index.html
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def ler_index():
    return FileResponse("static/index.html")
