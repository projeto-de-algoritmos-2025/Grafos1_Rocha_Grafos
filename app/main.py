from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import os

app = FastAPI()

# Caminho do dataset
DATA_PATH = os.path.join("data", "taco-db-nutrientes.parquet")

# Carrega os dados uma vez ao iniciar
df = pd.read_parquet(DATA_PATH)
df["Nome"] = df["Nome"].str.lower()

# Monta a pasta de arquivos estáticos (css, js, etc.)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Serve o index.html na raiz
@app.get("/", response_class=HTMLResponse)
def serve_home():
    with open(os.path.join("frontend", "index.html"), encoding="utf-8") as f:
        return f.read()

# Rota de busca (autocomplete)
@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    termos = q.lower()
    resultados = df[df["Nome"].str.contains(termos)]["Nome"].drop_duplicates().tolist()
    return resultados

# Rota de substituição
@app.get("/substitutes")
def get_substitutes(alimento: str):
    alimento = alimento.lower()

    if alimento not in df["Nome"].values:
        return JSONResponse(status_code=404, content={"erro": "Alimento não encontrado"})

    info_alimento = df[df["Nome"] == alimento].iloc[0]

    # Exemplo simples: pega 5 alimentos mais similares por proteína
    df["diff"] = (df["Proteína (g)"] - info_alimento["Proteína (g)"]).abs()
    similares = df[df["Nome"] != alimento].sort_values(by="diff").head(5)

    substitutos = []
    for _, row in similares.iterrows():
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

