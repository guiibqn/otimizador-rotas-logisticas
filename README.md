# 🐜 Otimização Logística com Colônia de Formigas (ACO)

Este projeto implementa uma meta-heurística de **Otimização por Colônia de Formigas (ACO)** aplicada a um problema complexo de logística: o roteamento inteligente de transportes sensível a custos variáveis.

O sistema simula o comportamento biológico de cooperação de formigas para encontrar a rota mais eficiente em um grafo, resolvendo variações do clássico Problema do Caixeiro Viajante (TSP).

> Desenvolvido como parte prática da disciplina de Inteligência Artificial.

## 📦 Tecnologias Utilizadas

- **Python 3.10+**
- **NumPy:** Manipulação de matrizes tridimensionais e cálculos probabilísticos vetorizados.
- **Matplotlib:** Plotagem visual do grafo e das rotas exploradas.

## 🦄 Funcionalidades e Modelagem de Negócio

Ao contrário de algoritmos simples de "menor caminho" (como Dijkstra puro), esta implementação modela um cenário logístico real ponderando múltiplos fatores conflitantes:

- **Custo de Pedágio (`W_PEDAGIO`):** Avalia se vale a pena pegar uma rota mais curta, porém mais cara devido a tarifas.
- **Tempo de Viagem (`W_TEMPO`):** Considera o impacto da duração da rota na produtividade.
- **Distância Física (`W_DISTANCIA`):** Avalia o consumo de combustível e desgaste da frota baseados na quilometragem.
- **Convergência Inteligente:** O algoritmo aprende com as iterações (via trilhas de feromônio), descartando rotas que são fisicamente viáveis, mas economicamente desvantajosas.

## 👩🏽‍💻 O Processo de Desenvolvimento

Comecei a modelagem definindo a estrutura de dados para representar as cidades e as diferentes conexões possíveis entre elas (rotas expressas vs. rotas normais). Usei matrizes tridimensionais (Origem x Destino x Tipo de Rota) com o NumPy para mapear as distâncias, tempos e custos de pedágio.

Em seguida, implementei o "coração" do algoritmo ACO: a função de transição de estado. Isso exigiu calcular as probabilidades de uma formiga escolher o próximo nó com base no nível de feromônio depositado e na visibilidade heurística (o quão "atraente" a rota é financeiramente).

O passo seguinte foi criar a rotina de atualização de feromônios. As rotas que resultavam em menor custo global recebiam mais feromônio (reforço positivo), enquanto o feromônio das outras rotas evaporava ao longo das iterações, forçando a colônia a convergir para a solução ótima.

Por fim, integrei o Matplotlib para gerar uma visualização clara do grafo, permitindo comparar visualmente as rotas exploradas pela colônia com o caminho ótimo final consolidado.

## 📚 O Que Eu Aprendi

Este projeto foi fundamental para aplicar conceitos avançados de Inteligência Artificial em um problema prático de negócios.

🧠 **Inteligência Artificial (Heurísticas):**
- Compreendi profundamente como algoritmos inspirados na natureza (Swarm Intelligence) podem resolver problemas de otimização combinatória (NP-hard) onde a busca por força bruta é inviável.

⚙️ **Modelagem Matemática e NumPy:**
- Aprimorei minha capacidade de modelar problemas complexos usando matrizes e aprendi a utilizar o NumPy para vetorizar cálculos de probabilidade, melhorando drasticamente a performance em relação a loops tradicionais em Python.

📊 **Análise de Múltiplos Fatores (Trade-offs):**
- Desenvolvi a habilidade de criar funções de avaliação (fitness) que equilibram variáveis conflitantes (ex: tempo vs. custo), uma habilidade crucial para o desenvolvimento de softwares corporativos de apoio à decisão.

## 🚀 Como Executar

1. Clone o repositório:
```bash
git clone [https://github.com/guiibqn/otimizador-rotas-logisticas.git](https://github.com/guiibqn/otimizador-rotas-logisticas.git)
