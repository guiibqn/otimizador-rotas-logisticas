import typing as tp
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURAÇÕES GERAIS ---
CIDADES: tp.Final[int] = 15
ROTAS: tp.Final[int] = 2  # 0 e 1

# Constantes do ACO
A: tp.Final[float] = 1.0 
B: tp.Final[float] = 1.0
R: tp.Final[float] = 0.5
Q: tp.Final[float] = 50.0

# Pesos do Custo Combinado
W_DISTANCIA: tp.Final[float] = 1.0 
W_PEDAGIO: tp.Final[float] = 2.0 
W_TEMPO: tp.Final[float] = 0.5 

# Inicialização de Arrays
cidades = np.arange(CIDADES)
inicio = np.copy(cidades)

tours = np.empty((CIDADES, CIDADES+1), dtype=int)
tours_rotas = np.empty((CIDADES, CIDADES+1), dtype=int) 

custos = np.zeros(CIDADES)
melhor_agente = -1
qtde_feromonio = np.zeros(CIDADES)

# ==============================================================================
# 1. DADOS E ESTRUTURA 3D
# ==============================================================================

# Listas originais
lista_distancia_cidades = [
    [0.0, 8.1, 3.4, 4.4, 7.0, 1.8, 9.9, 5.4, 2.5, 6.1, 8.7, 9.0, 1.2, 5.5, 7.3],
    [8.1, 0.0, 5.7, 2.0, 1.6, 6.7, 6.3, 4.1, 8.6, 4.2, 5.1, 5.5, 7.7, 2.1, 4.0],
    [3.4, 5.7, 0.0, 1.1, 6.2, 2.3, 6.5, 2.0, 4.0, 2.8, 8.1, 9.3, 3.1, 3.3, 6.0],
    [4.4, 2.0, 1.1, 0.0, 5.2, 3.0, 7.0, 2.5, 5.0, 2.5, 7.3, 8.1, 4.0, 1.4, 5.1],
    [7.0, 1.6, 6.2, 5.2, 0.0, 5.6, 5.0, 3.0, 7.5, 3.1, 4.0, 4.1, 6.7, 1.1, 2.9],
    [1.8, 6.7, 2.3, 3.0, 5.6, 0.0, 8.5, 3.9, 2.6, 4.7, 7.5, 8.2, 1.0, 4.1, 6.1],
    [9.9, 6.3, 6.5, 7.0, 5.0, 8.5, 0.0, 4.6, 9.4, 4.0, 2.0, 1.2, 9.1, 5.4, 4.2],
    [5.4, 4.1, 2.0, 2.5, 3.0, 3.9, 4.6, 0.0, 5.9, 1.0, 5.9, 6.7, 5.0, 2.1, 3.8],
    [2.5, 8.6, 4.0, 5.0, 7.5, 2.6, 9.4, 5.9, 0.0, 6.6, 8.7, 9.0, 2.0, 6.0, 7.4],
    [6.1, 4.2, 2.8, 2.5, 3.1, 4.7, 4.0, 1.0, 6.6, 0.0, 6.3, 6.9, 5.7, 2.3, 3.9],
    [8.7, 5.1, 8.1, 7.3, 4.0, 7.5, 2.0, 5.9, 8.7, 6.3, 0.0, 1.9, 7.9, 4.3, 2.8],
    [9.0, 5.5, 9.3, 8.1, 4.1, 8.2, 1.2, 6.7, 9.0, 6.9, 1.9, 0.0, 8.2, 4.7, 3.0],
    [1.2, 7.7, 3.1, 4.0, 6.7, 1.0, 9.1, 5.0, 2.0, 5.7, 7.9, 8.2, 0.0, 4.6, 6.5],
    [5.5, 2.1, 3.3, 1.4, 1.1, 4.1, 5.4, 2.1, 6.0, 2.3, 4.3, 4.7, 4.6, 0.0, 2.7],
    [7.3, 4.0, 6.0, 5.1, 2.9, 6.1, 4.2, 3.8, 7.4, 3.9, 2.8, 3.0, 6.5, 2.7, 0.0]
]

lista_pedagios = [
    [0.0, 2.5, 0.0, 1.0, 0.0, 0.0, 4.0, 1.5, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
    [2.5, 0.0, 3.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
    [0.0, 3.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0],
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 1.5],
    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0],
    [1.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0],
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    [0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1.5, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 1.0, 0.0, 0.0]
]

# Feromonios iniciais
lista_feromonios = [
    [9.99, 0.32, 0.18, 0.25, 0.39, 0.35, 0.17, 0.25, 0.16, 0.35, 0.32, 0.18, 0.45, 0.21, 0.12],
    [0.32, 9.99, 0.25, 0.37, 0.45, 0.29, 0.26, 0.30, 0.31, 0.32, 0.18, 0.20, 0.43, 0.30, 0.20],
    [0.18, 0.25, 9.99, 0.35, 0.31, 0.23, 0.42, 0.39, 0.32, 0.29, 0.14, 0.26, 0.25, 0.22, 0.17],
    [0.25, 0.37, 0.35, 9.99, 0.33, 0.36, 0.18, 0.39, 0.23, 0.23, 0.28, 0.17, 0.30, 0.25, 0.44],
    [0.39, 0.45, 0.31, 0.33, 9.99, 0.31, 0.38, 0.28, 0.30, 0.24, 0.25, 0.41, 0.20, 0.24, 0.20],
    [0.35, 0.29, 0.23, 0.36, 0.31, 9.99, 0.29, 0.38, 0.26, 0.16, 0.32, 0.34, 0.44, 0.46, 0.35],
    [0.17, 0.26, 0.42, 0.18, 0.38, 0.29, 9.99, 0.48, 0.30, 0.17, 0.28, 0.30, 0.36, 0.42, 0.16],
    [0.25, 0.30, 0.39, 0.39, 0.28, 0.38, 0.48, 9.99, 0.34, 0.37, 0.18, 0.21, 0.33, 0.43, 0.25],
    [0.16, 0.31, 0.32, 0.23, 0.30, 0.26, 0.30, 0.34, 9.99, 0.34, 0.36, 0.46, 0.31, 0.29, 0.27],
    [0.35, 0.32, 0.29, 0.23, 0.24, 0.16, 0.17, 0.37, 0.34, 9.99, 0.16, 0.39, 0.33, 0.21, 0.24],
    [0.32, 0.18, 0.14, 0.28, 0.25, 0.32, 0.28, 0.18, 0.36, 0.16, 9.99, 0.29, 0.26, 0.42, 0.27],
    [0.18, 0.20, 0.26, 0.17, 0.41, 0.34, 0.30, 0.21, 0.46, 0.39, 0.29, 9.99, 0.37, 0.32, 0.35],
    [0.45, 0.43, 0.25, 0.30, 0.20, 0.44, 0.36, 0.33, 0.31, 0.33, 0.26, 0.37, 9.99, 0.26, 0.27],
    [0.21, 0.30, 0.22, 0.25, 0.24, 0.46, 0.42, 0.43, 0.29, 0.21, 0.42, 0.32, 0.26, 9.99, 0.35],
    [0.12, 0.20, 0.17, 0.44, 0.20, 0.35, 0.16, 0.25, 0.27, 0.24, 0.27, 0.35, 0.27, 0.35, 9.99]
]

# --- PREENCHIMENTO DAS MATRIZES 3D ---
distancia_cidades = np.zeros((CIDADES, CIDADES, ROTAS))
pedagios = np.zeros((CIDADES, CIDADES, ROTAS))
tempos = np.zeros((CIDADES, CIDADES, ROTAS))
feromonios = np.ones((CIDADES, CIDADES, ROTAS)) 

# ROTA 0 (Dados Originais)
distancia_cidades[:, :, 0] = lista_distancia_cidades
pedagios[:, :, 0] = lista_pedagios
tempos[:, :, 0] = distancia_cidades[:, :, 0] * 1.0 
feromonios[:, :, 0] = lista_feromonios 

# ROTA 1 (Dados Alternativos - Lento e Sem Pedágio)
distancia_cidades[:, :, 1] = distancia_cidades[:, :, 0] * 1.5 
tempos[:, :, 1] = tempos[:, :, 0] * 2.0 
pedagios[:, :, 1] = 0.0 
feromonios[:, :, 1] = lista_feromonios 

# Diagonal Zero
for k in range(ROTAS):
    np.fill_diagonal(distancia_cidades[:, :, k], 0)
    np.fill_diagonal(pedagios[:, :, k], 0)
    np.fill_diagonal(tempos[:, :, k], 0)

# Mapa visual
mapa_cidades = np.array([
    [2, 2], 
    [2, 5], 
    [3, 7], 
    [4, 4], 
    [5, 1], 
    [5, 6], 
    [6, 3], 
    [7, 7], 
    [8, 2], 
    [8, 5], 
    [4, 9], 
    [9, 9], 
    [1, 7], 
    [6, 9], 
    [9, 1], 
    [2, 2]
])

# ==============================================================================
# 2. FUNÇÕES ACO
# ==============================================================================

def prox_cidade(_atual, _tour):
    candidatos_cidades = []
    candidatos_rotas = []
    probabilidades = []
    denominador = 0.0

    for c in range(CIDADES):
        if c not in _tour:
            for r in range(ROTAS):
                # Recupera dados 3D
                d = distancia_cidades[_atual][c][r]
                p = pedagios[_atual][c][r]
                t = tempos[_atual][c][r]

                # Custo Combinado
                custo = (d * W_DISTANCIA) + (p * W_PEDAGIO) + (t * W_TEMPO)
                if custo <= 0.0001: custo = 0.0001

                heuristica = 1.0 / custo
                feromonio = feromonios[_atual][c][r]

                # Score Probabilístico
                score = (feromonio ** A) * (heuristica ** B)

                candidatos_cidades.append(c)
                candidatos_rotas.append(r)
                probabilidades.append(score)
                denominador += score

    if len(candidatos_cidades) == 0:
        return -1, -1

    # Roleta (Probabilística)
    probabilidades = np.array(probabilidades)
    if denominador > 0:
        probabilidades = probabilidades / denominador
    else:
        
        probabilidades = np.ones(len(probabilidades)) / len(probabilidades)

    escolha_idx = np.random.choice(len(candidatos_cidades), p=probabilidades)
    
    return candidatos_cidades[escolha_idx], candidatos_rotas[escolha_idx]


def custos_tours():
    global custos
    global melhor_agente

    custos.fill(0)
    for f in range(CIDADES):
        for a in range(CIDADES):
            origem = tours[f][a].astype(int)
            destino = tours[f][a+1].astype(int)
            rota = tours_rotas[f][a+1].astype(int) 

            d = distancia_cidades[origem][destino][rota]
            p = pedagios[origem][destino][rota]
            t = tempos[origem][destino][rota]

            custos[f] += (d * W_DISTANCIA) + (p * W_PEDAGIO) + (t * W_TEMPO)

    print(f"Custos da rodada: {np.round(custos, 2)}")
    
    
    melhor_agente = np.argmin(custos)
    
    # Calcula quantidade de feromonio a depositar
    for a in range(CIDADES):
        if custos[a] > 0:
            qtde_feromonio[a] = Q / custos[a]
    
    print(f"Melhor Agente: {melhor_agente} | Custo: {custos[melhor_agente]:.2f}")


def atualiza_feromonio():
    global feromonios

    # 1. Evaporação
    feromonios = feromonios * (1 - R)
    feromonios[feromonios < 0.01] = 0.01 

    # 2. Depósito (Elitista)
    agente = melhor_agente
    
    for m in range(CIDADES):
        origem = tours[agente][m].astype(int)
        destino = tours[agente][m+1].astype(int)
        rota = tours_rotas[agente][m+1].astype(int)

        # Deposito simétrico
        feromonios[origem][destino][rota] += qtde_feromonio[agente]
        feromonios[destino][origem][rota] += qtde_feromonio[agente]

    print(f"Max Feromonio: {np.max(feromonios):.4f}")


# ==============================================================================
# 3. LOOP PRINCIPAL
# ==============================================================================

ITERACOES = 10

for i in range(ITERACOES):
    print(f"\n--- Iteracao {i+1} ---")
    tours.fill(-1)
    tours_rotas.fill(-1)
    np.random.shuffle(inicio)

    for f in range(CIDADES):        
        t = 0
        tours[f][t] = inicio[f]

        while(True):
            t = t+1
            if(t < CIDADES):
                prox, rota = prox_cidade(tours[f][t-1].astype(int), tours[f])
                tours[f][t] = prox
                tours_rotas[f][t] = rota
            else:
                # Volta ao inicio
                tours[f][t] = inicio[f]
                
                # Decide rota final (força bruta comparativa para o último passo)
                ultimo = tours[f][t-1].astype(int)
                primeiro = inicio[f]
                
                c0 = (distancia_cidades[ultimo][primeiro][0]*W_DISTANCIA + pedagios[ultimo][primeiro][0]*W_PEDAGIO)
                c1 = (distancia_cidades[ultimo][primeiro][1]*W_DISTANCIA + pedagios[ultimo][primeiro][1]*W_PEDAGIO)
                
                rota_final = 0 if c0 < c1 else 1
                tours_rotas[f][t] = rota_final
                break

    custos_tours()
    atualiza_feromonio()

# Plotagem
print("\nMelhor Tour Final:", tours[melhor_agente])
plt.figure(figsize=(10, 6))
x, y = mapa_cidades.T

# 1. Desenha as CIDADES
plt.plot(x, y, 'ko', markersize=8)

# 2. Adiciona os NOMES
nomes_cidades = [chr(65 + i) for i in range(CIDADES)]
for i in range(CIDADES):
    plt.annotate(nomes_cidades[i], (x[i], y[i]), xytext=(x[i]+0.1, y[i]+0.1), 
                 bbox=dict(boxstyle="round", alpha=0.1), color="red", size=12, fontweight="bold")

# 3. Desenha TODAS as formigas (Verde)
graph = np.empty((CIDADES+1, 2))
for f in range(CIDADES):
    for c in range(CIDADES+1):
        idx = tours[f][c].astype(int)
        graph[c] = mapa_cidades[idx]
    
    xg, yg = graph.T
    plt.plot(xg, yg, linestyle='dashed', color='green', alpha=0.3) 

# 4. Desenha o MELHOR AGENTE (Azul)
graph_melhor = np.empty((CIDADES+1, 2))
for c in range(CIDADES+1):
    idx = tours[melhor_agente][c].astype(int)
    graph_melhor[c] = mapa_cidades[idx]

xg, yg = graph_melhor.T
plt.plot(xg, yg, 'b-', linewidth=2, label=f"Melhor Caminho (Custo {custos[melhor_agente]:.2f})")

plt.title("ACO com Pedágios: Todas as Rotas (Verde) vs Melhor (Azul)")
plt.legend()
plt.show()