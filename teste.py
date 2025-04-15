import pandas as pd
from collections import deque

# Carregar o dataset
df = pd.read_parquet("taco-db-nutrientes.parquet")

# Colunas de interesse
nutrientes = ['Proteína (g)', 'Lipídeos (g)', 'Carboidrato (g)', 'Fibra Alimentar (g)', 'Cálcio (mg)']

# Garantir conversão numérica
for col in nutrientes:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Função para calcular a distância (similaridade nutricional)
def calcular_similaridade(a1, a2):
    return sum(abs(a1[n] - a2[n]) for n in nutrientes)

# Construir grafo totalmente conectado com pesos
grafo = {}
for i, a1 in df.iterrows():
    nome1 = a1['Nome']
    grafo[nome1] = []
    for j, a2 in df.iterrows():
        if i != j:
            nome2 = a2['Nome']
            distancia = calcular_similaridade(a1, a2)
            grafo[nome1].append((nome2, distancia))  # vizinho com peso

# Função de BFS com limite de substituições
def substitutos_bfs(inicio, max_resultados=5):
    if inicio not in grafo:
        return []

    visitados = set()
    fila = deque([inicio])
    substitutos = []

    while fila and len(substitutos) < max_resultados:
        atual = fila.popleft()
        if atual not in visitados:
            visitados.add(atual)
            vizinhos_ordenados = sorted(grafo[atual], key=lambda x: x[1])  # vizinhos mais próximos primeiro
            for vizinho, dist in vizinhos_ordenados:
                if vizinho not in visitados:
                    fila.append(vizinho)
                    substitutos.append((vizinho, dist))
                    if len(substitutos) >= max_resultados:
                        break
    return substitutos

# Teste
alimento_escolhido = "Arroz integral cozido"
resultado = substitutos_bfs(alimento_escolhido)

if resultado:
    print(f"\nAlimento escolhido: {alimento_escolhido}")
    print("Substitutos encontrados:")
    for nome_parecido, distancia in resultado:
        print(f"🔸 {nome_parecido} (distância: {distancia:.2f})")

    # Comparar com o mais parecido
    nome_parecido, distancia = resultado[0]
    print("\n--- Informações nutricionais comparadas ---")
    dados_escolhido = df[df['Nome'] == alimento_escolhido][nutrientes].values[0]
    dados_parecido = df[df['Nome'] == nome_parecido][nutrientes].values[0]

    for i, n in enumerate(nutrientes):
        print(f"{n}: {alimento_escolhido} = {dados_escolhido[i]} | {nome_parecido} = {dados_parecido[i]}")
else:
    print("Nenhum substituto encontrado.")

