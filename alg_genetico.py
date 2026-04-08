import numpy as np
import random
import matplotlib.pyplot as plt
import os

# --- FUNÇÕES - devem vir primeiro ---

def criar_população(tamanho):
    #gera 2 numeros aleatório entre -10 e 10  (x e y) com 2 casas decimais e vírgula com tamanho dinâmico
    return [[round(random.uniform(-10, 10), 2), round(random.uniform(-10, 10), 2)] for _ in range(tamanho)]

def fitness(x, y):
    # apenas retornei a própria Fórmula de Schaffer's f6 disponibilizada no slide
    temp1 = np.sin(np.sqrt(x**2 + y**2))**2 - 0.5
    temp2 = (1.0 + 0.001 * (x**2 + y**2))**2
    return 0.5 - (temp1 / temp2)

def calcula_fitness(populacao):
    return [fitness(ind[0], ind[1]) for ind in populacao]

def mutar_individuos(individuo, taxa_mutacao=0.05):
    for i in range(len(individuo)):
        #random.random gera um aleatório entre 0 e 1 (nunca 1)
        if random.random() < taxa_mutacao:
            # Sorteia um valor da curva de Gauss e soma ao x ou y atual
            #  mu=0 e sigma=0.5 (um passo médio)
            ruido = random.gauss(0, 0.5) #funcao do próprio python para gerar o valor gaussiano pedido 
            individuo[i] += ruido
        
        #apenas uma restrição para não sair do próprio valor para as coordenadas definido anteriormente
        if individuo[i] > 10: individuo[i] = 10
        if individuo[i] < -10: individuo[i] = -10
    return individuo

def selecao_torneio(populacao, fitnesses, k=3):
    #seleciona aleatoriamente
    selecionados_indices = random.sample(range(len(populacao)), k)
    melhor_indice = selecionados_indices[0]
    #procura o "best"
    for idx in selecionados_indices:
        if fitnesses[idx] > fitnesses[melhor_indice]:
            melhor_indice = idx
    return populacao[melhor_indice]

def crossover(pai1, pai2, taxa_crossover=0.8, alpha=0.5):
    # O crossover só ocorre baseado na taxa
    if random.random() < taxa_crossover:
        filho_x = alpha * pai1[0] + (1 - alpha) * pai2[0]
        filho_y = alpha * pai1[1] + (1 - alpha) * pai2[1]
        return [filho_x, filho_y]
    else:
        return random.choice([pai1, pai2]).copy()

# --- plotagem dos gráficos ---

def plotar_geracao(populacao, geracao, pasta="frames"):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    # 1. Cria a grade para as curvas de nível
    x_range = np.linspace(-10, 10, 100)
    y_range = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(x_range, y_range)
    Z = fitness(X, Y)

    plt.figure(figsize=(10, 8))
    
    # 2. Desenha as curvas de nível ao fundo
    contorno = plt.contourf(X, Y, Z, levels=50, cmap='viridis')
    plt.colorbar(contorno, label='Fitness')

    # 3. Plota os indivíduos da população atual
    pop_x = [ind[0] for ind in populacao]
    pop_y = [ind[1] for ind in populacao]
    plt.scatter(pop_x, pop_y, color='red', edgecolors='white', s=30, label='População')

    plt.title(f"Algoritmo Genético - Schaffer's f6\nGeração: {geracao}")
    plt.xlabel("Eixo X")
    plt.ylabel("Eixo Y")
    plt.legend()
    
    # Salva o frame --> para o vídeo 
    plt.savefig(f"{pasta}/geracao_{geracao:03d}.png")
    plt.close()

# --- EXECUÇÃO ---

TAMANHO_POP = 100
GERACOES = 100
TAXA_CROSS = 0.8
TAXA_MUT = 0.05

populacao = criar_população(TAMANHO_POP)

for g in range(GERACOES):
    fits = calcula_fitness(populacao)
    
    # Salvar o gráfico da geração atual
    if g % 5 == 0 or g == GERACOES - 1: # Plota a cada 5 gerações para teste rápido
        plotar_geracao(populacao, g)

    melhor_da_geracao = populacao[np.argmax(fits)].copy()
    nova_populacao = [melhor_da_geracao] # Elitismo [cite: 785]

    while len(nova_populacao) < TAMANHO_POP:
        p1 = selecao_torneio(populacao, fits)
        p2 = selecao_torneio(populacao, fits)
        filho = crossover(p1, p2, TAXA_CROSS)
        filho = mutar_individuos(filho, TAXA_MUT)
        nova_populacao.append(filho)
    
    populacao = nova_populacao
    print(f"Geração {g}: Melhor Fitness = {max(fits):.4f}")

print("\nImagens salvas na pasta 'frames'.")