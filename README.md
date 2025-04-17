# Grafos1_Rocha_Grafos

**Número da Lista**: 1<br>
**Conteúdo da Disciplina**:Grafos 1<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 22/2022000  | Milena Fernandes Rocha |
| 20/2045348  | Ingrid Alves Rocha |

## Sobre 
Este projeto utiliza a estrutura de dados de grafos e o algoritmo Breadth-First Search (BFS) para analisar e visualizar as relações entre diferentes alimentos com base em suas características nutricionais e propriedades. O sistema permite explorar conexões entre alimentos, descobrir caminhos de similaridade e identificar grupos de alimentos com propriedades semelhantes.

## Screenshots
<!-- Colocar os prints de aceitos aqui -->


## Linguagem 
- Python
- C++

## Estrutura do Grafo

1. **Construção do Grafo**:
   - O grafo é representado como um dicionário (`grafo = {}`) onde:
     - Chaves: Nomes dos alimentos (vértices)
     - Valores: Listas de tuplas representando arestas (alimento conectado, distância/similaridade)

2. **Cálculo de Similaridade**:
   - A função `calcular_similaridade(a1, a2)` computa a distância entre dois alimentos baseada em 5 nutrientes:
     ```python
     nutrientes = ['Proteína (g)', 'Lipídeos (g)', 'Carboidrato (g)', 'Fibra Alimentar (g)', 'Cálcio (mg)']
     ```
   - Quanto menor a distância, mais similares são os alimentos

## Algoritmo BFS Implementado

A função `substitutos_bfs(inicio, max_resultados=5)` implementa:

1. **Inicialização**:
   - Verifica se o alimento inicial existe no grafo
   - Cria estruturas para controle:
     - `visitados`: conjunto de alimentos já processados
     - `fila`: deque para gerenciar a ordem de processamento
     - `substitutos`: lista de resultados

2. **Processamento BFS**:
   - Utiliza uma fila para processar alimentos em largura
   - Para cada alimento (`atual`):
     - Ordena seus vizinhos por similaridade (menor distância primeiro)
     - Adiciona os vizinhos não visitados à fila
     - Coleta informações nutricionais dos substitutos encontrados

3. **Critério de Parada**:
   - Para quando encontra `max_resultados` substitutos ou quando a fila esvazia

## Fluxo da Aplicação FastAPI

1. **Endpoint `/search`**:
   - Busca alimentos por nome (case insensitive)
   - Retorna lista de nomes correspondentes

2. **Endpoint `/substitutes`**:
   - Chama `substitutos_bfs` para o alimento solicitado
   - Retorna estrutura com:
     - Informações do alimento inicial
     - Lista de substitutos ordenados por similaridade
     - Informações nutricionais de cada substituto

## Pontos Fortes da Implementação

1. **Ordenação por Similaridade**:
   ```python
   vizinhos_ordenados = sorted(grafo[atual], key=lambda x: x[1])
   ```
   - Garante que os substitutos mais similares sejam considerados primeiro

2. **Estrutura de Retorno Rica**:
   - Inclui tanto a distância quanto os dados nutricionais completos

3. **Controle de Visitados**:
   - Evita ciclos infinitos e reprocessamento

<!-- ## Uso 
Explique como acessar o exércicio proposto

