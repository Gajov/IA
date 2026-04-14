# 📘 Algoritmo Genético com Mutação Adaptativa

## 📌 Visão Geral

Este projeto implementa um **Algoritmo Genético (AG)** para otimização da função **Schaffer F6**, um problema clássico multimodal com vários ótimos locais.

O objetivo é encontrar o **máximo global da função**, utilizando técnicas evolutivas como:

- Seleção por torneio  
- Crossover aritmético  
- Mutação gaussiana  
- Elitismo  
- Mutação adaptativa baseada em diversidade  

---

## ⚙️ Configurações

```python
TAMANHO_POP = 300
GERACOES = 61
TAXA_CROSS = 0.8
TAXA_MUT = 0.5
MAXMUT = 2.5
ELITESIZE = 10
TORNEIOSIZE = 5
FRM = 6
PLOT = 'off'
```

### 🔍 Parâmetros

- **TAMANHO_POP**: número de indivíduos por geração  
- **GERACOES**: número total de gerações  
- **TAXA_CROSS**: probabilidade de crossover  
- **TAXA_MUT**: taxa base de mutação  
- **MAXMUT**: intensidade máxima da mutação (desvio padrão)  
- **ELITESIZE**: número de indivíduos preservados  
- **TORNEIOSIZE**: tamanho do torneio  
- **FRM**: controla o decaimento da mutação  
- **PLOT**: ativa/desativa visualização  

---

## 🧬 Representação

Cada indivíduo é um vetor:

```python
[x, y]
```

Onde:

- x, y ∈ [-10, 10]

---

## 🎯 Função Objetivo

A função Schaffer F6:

- Possui múltiplos ótimos locais  
- Ótimo global ≈ 1  
- Desafiadora para algoritmos de busca  

---

## 🔧 Etapas do Algoritmo

### 1. Inicialização

- População aleatória no intervalo [-10, 10]

---

### 2. Avaliação de Fitness

- Mede a qualidade de cada indivíduo  
- Quanto maior, melhor  

---

### 3. Seleção (Torneio)

- Seleciona `k` indivíduos aleatórios  
- Retorna o melhor  

✔ Simples e eficiente  

---

### 4. Crossover

Crossover aritmético:

```
filho = α * pai1 + (1 - α) * pai2
```

- Gera dois filhos interpolando os pais  

---

### 5. Mutação

- Ruído gaussiano:
  - Média = 0  
  - Desvio = MAXMUT  
- Mantém valores no intervalo permitido  

---

## 🔥 Mutação Adaptativa

A taxa de mutação varia conforme:

### 🕒 Tempo (gerações)

```python
x = g / (GERACOES - 5)
decay = (1 - x**FRM)
```

- Reduz a mutação ao longo do tempo  
- FRM controla o formato da curva  

---

### 🌍 Diversidade da população

```python
delta = (melhor_f - fit_medio) / (abs(melhor_f) + 1e-7)
```

- Mede o quão homogênea está a população  

---

### ⚡ Fórmula final

```python
TAXA_MUT_G = decay * TAXA_MUT * np.exp(-delta)
```

### 🧠 Interpretação

- População homogênea → mutação aumenta  
- População diversa → mutação diminui  
- Gerações avançadas → mutação diminui  

✔ Balanceia exploração e refinamento  

---

## 🏆 Elitismo

- Mantém os melhores indivíduos  
- Evita perda de boas soluções  

---

## 🔁 Loop Evolutivo

Para cada geração:

1. Avalia fitness  
2. Aplica elitismo  
3. Seleciona pais  
4. Aplica crossover  
5. Aplica mutação  
6. Gera nova população  

---

## 🎯 Critério de Sucesso

```python
if melhor_f > 0.9904:
```

- Considera solução próxima do ótimo global  

---

## 🔄 Execução

- O algoritmo roda 100 vezes  
- Calcula a taxa de sucesso  

---

## 📈 Visualização (Opcional)

### 🖼️ Frames

- Mostram a evolução da população ao longo das gerações  

### 🎞️ GIF

- Arquivo gerado: `evolucao.gif`  

---

### 📊 Gráfico Final

- Arquivo gerado: `evolucao_fitness.png`  

Mostra:

- Melhor fitness por geração  
- Fitness médio  

---

## 📊 Interpretação dos Resultados

- Convergência rápida → algoritmo eficiente  
- Fitness médio próximo do melhor → população convergiu  
- Oscilações → exploração ativa  

---

## 🚀 Melhorias Possíveis

- Mutação adaptativa por indivíduo  
- Crossover avançado (BLX-α, SBX)  
- Reinicialização parcial da população  
- Paralelização  

---

## 🧠 Conclusão

O algoritmo combina:

- Técnicas clássicas de algoritmos genéticos  
- Controle adaptativo da taxa de mutação  
- Estratégias de exploração e refinamento  

✔ Resultado: método robusto para otimização em espaços complexos e multimodais
