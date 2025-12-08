# Otimização Logística com Colônia de Formigas

Este projeto consiste na implementação de uma meta-heurística de **Otimização por Colônia de Formigas (ACO)** aplicada à solução de um problema complexo de logística: o roteamento inteligente de transportes sensível a custos variáveis.

O sistema simula o comportamento biológico de cooperação de formigas (através de trilhas de feromônio) para encontrar a rota mais eficiente em um grafo, resolvendo variações do clássico **Problema do Caixeiro Viajante (TSP)**.

> Desenvolvido como parte prática da disciplina de **Inteligência Artificial / Otimização**.

## O Problema de Negócio Modelado

Ao contrário de algoritmos simples de "menor caminho" (como Dijkstra puro), esta implementação modela um cenário logístico real onde a decisão deve ponderar múltiplos fatores conflitantes:

- **Custo de Pedágio (`W_PEDAGIO`):** O sistema avalia se vale a pena pegar uma rota mais curta, porém mais cara devido a tarifas.
- **Tempo de Viagem (`W_TEMPO`):** Considera o impacto da duração da rota na produtividade, diferenciando rotas expressas de rotas lentas.
- **Distância Física (`W_DISTANCIA`):** O consumo de combustível e desgaste da frota baseados na quilometragem.
- **Convergência Inteligente:** O algoritmo aprende com as iterações (feromônio), descartando rotas que são tecnicamente viáveis, mas economicamente inviáveis.

## Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **NumPy:** Utilizado para manipulação de matrizes tridimensionais (Origem x Destino x Tipo de Rota) e cálculos probabilísticos vetorizados.
- **Matplotlib:** Para plotagem visual do grafo, demonstrando as rotas exploradas pela colônia (verde) versus a solução ótima consolidada (azul).

## Como Executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
2. Execute a simulação:
    ```bash
    python main.py

## Saída do Sistema
O sistema exibe o progresso das gerações no terminal, mostrando a redução progressiva do custo logístico à medida que a colônia converge. Ao final, é gerado um mapa visual destacando o "Caminho Ótimo" encontrado pela inteligência coletiva dos agentes.

## Autor
Guilherme Augusto Boquimpani