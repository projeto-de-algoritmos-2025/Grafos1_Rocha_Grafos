from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from collections import deque
import pandas as pd
import os

app = FastAPI()


DATA_PATH = os.path.join("data", "taco-db-nutrientes.parquet")

df = pd.read_parquet(DATA_PATH)
df["Nome"] = df["Nome"].str.lower()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/", response_class=HTMLResponse)
def serve_home():
    with open(os.path.join("frontend", "index.html"), encoding="utf-8") as f:
        return f.read()

@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    termos = q.lower()
    resultados = df[df["Nome"].str.contains(termos)]["Nome"].drop_duplicates().tolist()
    return resultados


def calcular_distancia(a, b):
    return sum((a[nutriente] - b[nutriente]) ** 2 for nutriente in [
        "Proteína (g)", "Lipídeos (g)", "Carboidrato (g)", "Fibra Alimentar (g)", "Cálcio (mg)"
    ]) ** 0.5
def construir_grafo(df):
    grafo = {}
    for i, row_a in df.iterrows():
        nome_a = row_a["Nome"]
        grafo[nome_a] = []
        for j, row_b in df.iterrows():
            nome_b = row_b["Nome"]
            if nome_a != nome_b:
                dist = calcular_distancia(row_a, row_b)
                grafo[nome_a].append((nome_b, dist))
        grafo[nome_a].sort(key=lambda x: x[1])
    return grafo

grafo_similaridade = construir_grafo(df)

@app.get("/substitutes")
def get_substitutes(alimento: str, k: int = 5):
    alimento = alimento.lower()

    if alimento not in df["Nome"].values:
        return JSONResponse(status_code=404, content={"erro": "Alimento não encontrado"})

    info_alimento = df[df["Nome"] == alimento].iloc[0]

    grafo = grafo_similaridade

    visitados = set()
    fila = deque()
    fila.append(alimento)
    visitados.add(alimento)

    substitutos = []
    while fila and len(substitutos) < k:
        atual = fila.popleft()
        for vizinho, _ in grafo[atual]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)

                row = df[df["Nome"] == vizinho].iloc[0]
                substitutos.append({
                    "nome": str(row["Nome"]),
                    "informacoes_nutricionais": {
                        "Proteína (g)": float(row["Proteína (g)"]),
                        "Lipídeos (g)": float(row["Lipídeos (g)"]),
                        "Carboidrato (g)": float(row["Carboidrato (g)"]),
                        "Fibra Alimentar (g)": float(row["Fibra Alimentar (g)"]),
                        "Cálcio (mg)": float(row["Cálcio (mg)"]),
                    }
                })

                if len(substitutos) >= k:
                    break

    return {
        "alimento_inicial": {
            "nome": str(info_alimento["Nome"]),
            "informacoes_nutricionais": {
                "Proteína (g)": float(info_alimento["Proteína (g)"]),
                "Lipídeos (g)": float(info_alimento["Lipídeos (g)"]),
                "Carboidrato (g)": float(info_alimento["Carboidrato (g)"]),
                "Fibra Alimentar (g)": float(info_alimento["Fibra Alimentar (g)"]),
                "Cálcio (mg)": float(info_alimento["Cálcio (mg)"]),
            }
        },
        "substitutos": substitutos
    }


