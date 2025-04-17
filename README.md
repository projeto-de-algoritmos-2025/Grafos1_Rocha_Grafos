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

## Como Executar o Projeto de Grafos de Alimentos

## Passo 1: Clonar o Repositório

Abra o terminal/command prompt e execute:

```bash
git clone https://github.com/projeto-de-algoritmos-2025/Grafos1_Rocha_Grafos.git
cd Grafos1_Rocha_Grafos
```

## Passo 2: Criar um Ambiente Virtual (Recomendado)

É boa prática criar um ambiente virtual para isolar as dependências:

```bash
python -m venv venv
```

Ative o ambiente virtual:

- No Windows:
  ```bash
  venv\Scripts\activate
  ```
- No Linux/MacOS:
  ```bash
  source venv/bin/activate
  ```

## Passo 3: Instalar as Dependências

Com o ambiente virtual ativado, instale os pacotes necessários:

```bash
pip install -r requirements.txt
```

(O projeto deve incluir um arquivo `requirements.txt` com todas as dependências. Se não tiver, instale manualmente:)
```bash
pip install fastapi pandas python-multipart uvicorn
```

## Passo 4: Baixar o Dataset

Verifique se o arquivo `taco-db-nutrientes.parquet` está na pasta raiz do projeto. Se não estiver, você precisará:

1. Baixar o dataset TACO (Tabela Brasileira de Composição de Alimentos)
2. Converter para o formato parquet (ou ajustar o código para ler o formato original)

## Passo 5: Executar a Aplicação

Inicie o servidor FastAPI com:

```bash
uvicorn main:app --reload
```

O `--reload` faz o servidor recarregar automaticamente quando você faz mudanças no código (ótimo para desenvolvimento).

## Passo 6: Acessar a Aplicação

A API estará disponível em:

- **API**: http://localhost:8000
- **Documentação interativa**:
  - Swagger UI: http://localhost:8000/docs
  - Redoc: http://localhost:8000/redoc

A interface web estará em http://localhost:8000/static/index.html

## Endpoints Principais

1. **Buscar alimentos**:
   ```
   GET /search?q=frango
   ```

2. **Obter substitutos**:
   ```
   GET /substitutes?alimento=Arroz%20integral%20cozido
   ```

## Executando com Docker (Opcional)

Se preferir usar Docker:

1. Certifique-se de ter o [Docker](https://docs.docker.com/get-docker/) instalado
2. Crie um arquivo Dockerfile (se não existir)
3. Execute:
   ```bash
   docker build -t alimento-grafos .
   docker run -d -p 8000:8000 alimento-grafos
   ```

<!-- ## Uso 
Explique como acessar o exércicio proposto

