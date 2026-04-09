import numpy as np
import random
import matplotlib.pyplot as plt
import os

# --- FUNÇÕES - devem vir primeiro ---

def criar_população(tamanho):
    # gera 2 numeros aleatório entre -10 e 10 (x e y) com 2 casas decimais e vírgula com tamanho dinâmico
    return [[round(random.uniform(-100, 100), 2), round(random.uniform(-100, 100), 2)] for _ in range(tamanho)]

def fitness(x, y):
    # apenas retornei a própria Fórmula de Schaffer's f6 disponibilizada no slide 89
    temp1 = np.sin(np.sqrt(x**2 + y**2))**2 - 0.5
    temp2 = (1.0 + 0.001 * (x**2 + y**2))**2
    return 0.5 - (temp1 / temp2)

def calcula_fitness(populacao):
    # avalia a qualidade de cada soluçao candidata (indivíduo) [cite: 39]
    return [fitness(ind[0], ind[1]) for ind in populacao]

def mutar_individuos(individuo, taxa_mutacao=0.05):
    # objetivo: manter a diversidade e evitar convergencia prematura [cite: 662, 663]
    for i in range(len(individuo)):
        # random.random gera um aleatório entre 0 e 1 (nunca 1)
        if random.random() < taxa_mutacao:
            # Sorteia um valor da curva de Gauss e soma ao x ou y atual
            # mu=0 e sigma=0.5 (um passo médio)
            ruido = random.gauss(0,5) # funcao do próprio python para gerar o valor gaussiano pedido [cite: 715, 747]
            individuo[i] += ruido
        
        # apenas uma restrição para não sair do próprio valor para as coordenadas definido anteriormente (solução viável) 
        if individuo[i] > 100: individuo[i] = 100
        if individuo[i] < -100: individuo[i] = -100
    return individuo

def selecao_torneio(populacao, fitnesses, k=3):
    # seleciona aleatoriamente k indivíduos e o melhor vence [cite: 373, 497]
    selecionados_indices = random.sample(range(len(populacao)), k)
    melhor_indice = selecionados_indices[0]
    # procura o "best" do grupo [cite: 378]
    for idx in selecionados_indices:
        if fitnesses[idx] > fitnesses[melhor_indice]:
            melhor_indice = idx
    return populacao[melhor_indice]

def crossover_aritmetico(pai1, pai2, alpha=0.5):
    # gera filhos combinando genes dos pais usando média ponderada [cite: 587, 626]
    f1_x = alpha * pai1[0] + (1 - alpha) * pai2[0]
    f1_y = alpha * pai1[1] + (1 - alpha) * pai2[1]
    
    f2_x = (1 - alpha) * pai1[0] + alpha * pai2[0]
    f2_y = (1 - alpha) * pai1[1] + alpha * pai2[1]
    
    return [f1_x, f1_y], [f2_x, f2_y]

# --- plotagem dos gráficos ---

def plotar_geracao(populacao, geracao, pasta="frames"):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    x_range = np.linspace(-20, 20, 400) # Zoom no centro para ver os anéis
    y_range = np.linspace(-20, 20, 400)
    X, Y = np.meshgrid(x_range, y_range)
    Z = fitness(X, Y)

    plt.figure(figsize=(10, 8))
    contorno = plt.contourf(X, Y, Z, levels=50, cmap='viridis')
    plt.colorbar(contorno, label='Fitness')

    pop_x = [ind[0] for ind in populacao]
    pop_y = [ind[1] for ind in populacao]
    plt.scatter(pop_x, pop_y, color='red', edgecolors='white', s=30, label='População')

    plt.title(f"Algoritmo Genético - Schaffer's f6\nGeração: {geracao}")
    plt.xlabel("Eixo X")
    plt.ylabel("Eixo Y")
    plt.savefig(f"{pasta}/geracao_{geracao:03d}.png")
    plt.close()

# --- EXECUÇÃO ---

TAMANHO_POP = 35
GERACOES = 20
TAXA_CROSS = 0.8
TAXA_MUT = 0.05
historico_fitness = []

populacao = criar_população(TAMANHO_POP)

for g in range(GERACOES):
    fits = calcula_fitness(populacao)
    melhor_f = max(fits)
    historico_fitness.append(melhor_f)
    
    if g % 5 == 0 or g == GERACOES - 1:
        plotar_geracao(populacao, g)

    # ELITISMO: os n melhores nunca são substituídos (tipicamente n=2) [cite: 785, 790, 874]
    indices_elite = np.argsort(fits)[-2:] 
    nova_populacao = [populacao[i].copy() for i in indices_elite]

    # 4. Criar o restante da nova geração (popsize - n deve ser par) [cite: 882, 896]
    while len(nova_populacao) < TAMANHO_POP:
        # Seleção de dois pais [cite: 898, 900]
        p1 = selecao_torneio(populacao, fits)
        p2 = selecao_torneio(populacao, fits)
        
        # Crossover gera dois filhos se a taxa permitir [cite: 616, 906]
        if random.random() < TAXA_CROSS:
            f1, f2 = crossover_aritmetico(p1, p2)
        else:
            f1, f2 = p1.copy(), p2.copy()
        
        # Mutação dos filhos [cite: 907]
        f1 = mutar_individuos(f1, TAXA_MUT)
        f2 = mutar_individuos(f2, TAXA_MUT)
        
        nova_populacao.append(f1)
        if len(nova_populacao) < TAMANHO_POP:
            nova_populacao.append(f2)
    
    populacao = nova_populacao
    print(f"Geração {g}: Melhor Fitness = {melhor_f:.4f}")

# Gráfico de evolução do fitness ao longo das gerações [cite: 86, 1150]
plt.figure()
plt.plot(historico_fitness)
plt.title("Evolução do Melhor Fitness")
plt.xlabel("Geração")
plt.ylabel("Fitness")
plt.grid(True)
plt.show()

print("\nImagens salvas na pasta 'frames'.")