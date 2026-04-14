import numpy as np
import random
import matplotlib.pyplot as plt
import os
import imageio.v2 as imageio

# ================= CONFIG =================
TAMANHO_POP = 200
GERACOES = 71
TAXA_CROSS = 0.9
TAXA_MUT = 0.5
MAXMUT = 2.5
ELITESIZE = 3
TORNEIOSIZE = 2
FRM = 6 # Fator de Regressão da Taxa de Mutação

# ==========================================

# --- FUNÇÕES ---

def criar_população(tamanho):
    return [[random.uniform(-10, 10), random.uniform(-10, 10)] for _ in range(tamanho)]

def fitness(x, y):
    temp1 = np.sin(np.sqrt(x**2 + y**2))**2 - 0.5
    temp2 = (1.0 + 0.001 * (x**2 + y**2))**2
    return 0.5 - (temp1 / temp2)

def calcula_fitness(populacao):
    return [fitness(ind[0], ind[1]) for ind in populacao]

def calcula_fitness_medio(populacao):
    return sum(fitness(ind[0], ind[1]) for ind in populacao) / len(populacao)

def mutar_individuos(individuo, taxa_mutacao):
    if random.random() < taxa_mutacao:
        for i in range(len(individuo)):
            individuo[i] += random.gauss(0,MAXMUT)
            individuo[i] = max(-10, min(10, individuo[i]))
    return individuo

def selecao_torneio(populacao, fitnesses, k=TORNEIOSIZE):
    selecionados = random.sample(range(len(populacao)), k)
    melhor = selecionados[0]

    for idx in selecionados:
        if fitnesses[idx] > fitnesses[melhor]:
            melhor = idx

    return populacao[melhor]

# --- CROSSOVERS ---

def crossover(p1, p2):
    alpha=random.uniform(0.25,0.75)
    f1 = [alpha*p1[0] + (1-alpha)*p2[0],
          alpha*p1[1] + (1-alpha)*p2[1]]

    f2 = [(1-alpha)*p1[0] + alpha*p2[0],
          (1-alpha)*p1[1] + alpha*p2[1]]

    return f1, f2


# --- PLOT ---

def plotar_geracao(populacao, geracao, pasta="frames"):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    x_range = np.linspace(-10, 10, 400)
    y_range = np.linspace(-10, 10, 400)
    X, Y = np.meshgrid(x_range, y_range)
    Z = fitness(X, Y)

    plt.figure(figsize=(10, 8))
    contorno = plt.contourf(X, Y, Z, levels=50, cmap='viridis')
    plt.colorbar(contorno)

    pop_x = [ind[0] for ind in populacao]
    pop_y = [ind[1] for ind in populacao]
    plt.scatter(pop_x, pop_y, color='red', edgecolors='white', s=30, label="População")

    # melhor indivíduo
    fits = calcula_fitness(populacao)
    best_idx = np.argmax(fits)
    best = populacao[best_idx]

    plt.scatter(best[0], best[1],
                color='yellow', edgecolors='black',
                s=120, marker='*', label="Melhor")

    plt.legend()
    plt.title(f"Geração {geracao}")
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.savefig(f"{pasta}/geracao_{geracao:03d}.png")
    plt.close()

# --- EXECUÇÃO ---
sucs = 0
for i in range(1):
    # limpa frames antigos
    if os.path.exists("frames"):
        for f in os.listdir("frames"):
            os.remove(os.path.join("frames", f))

    historico_fitness = []
    historico_fitness_medio = []

    populacao = criar_população(TAMANHO_POP)

    melhor_f = 0
    fit_medio = 0
    for g in range(GERACOES):
        #TAXA_MUT_G = TAXA_MUT * max(0,(1-(g/(GERACOES-5))**FRM))
        # normaliza tempo
        x = g / (GERACOES - 10)

        # decaimento temporal (controla convergência final)
        decay = (1 - x**FRM)

        # diferença entre melhor e médio (estado da população)
        delta = (melhor_f - fit_medio) / (abs(melhor_f)+0.0000001)

        # mutação adaptativa + decaimento
        TAXA_MUT_G = max(0.0,decay * (0 + (TAXA_MUT - 0) * np.exp(-5 * delta)))

        fits = calcula_fitness(populacao)
        fit_medio = calcula_fitness_medio(populacao)
        melhor_f = max(fits)

        historico_fitness.append(melhor_f)
        historico_fitness_medio.append(fit_medio)

        if g % 2 == 0 or g == GERACOES - 1:
            plotar_geracao(populacao, g)

        # elitismo
        elite_idx = np.argsort(fits)[-ELITESIZE:]
        nova_pop = [populacao[i].copy() for i in elite_idx]


        while len(nova_pop) < TAMANHO_POP:
            p1 = selecao_torneio(populacao, fits)
            p2 = selecao_torneio(populacao, fits)

            if random.random() < TAXA_CROSS:
                    f1, f2 = crossover(p1, p2)
            else:
                f1, f2 = p1.copy(), p2.copy()

            f1 = mutar_individuos(f1,TAXA_MUT_G)
            f2 = mutar_individuos(f2, TAXA_MUT_G)

            nova_pop.append(f1)
            if len(nova_pop) < TAMANHO_POP:
                nova_pop.append(f2)

        populacao = nova_pop

        print(f"Geracao {g}: Melhor={melhor_f:.6f} | Medio={fit_medio:.6} | TAXAMUT={TAXA_MUT_G:.2}")
    if melhor_f>0.9904:
        sucs += 1 

print(f"Taxa de sucesso: {sucs}%")

# --- GIF ---

images = []
for arquivo in sorted(os.listdir("frames")):
    if arquivo.endswith(".png"):
        images.append(imageio.imread(os.path.join("frames", arquivo)))

imageio.mimsave("evolucao.gif", images, duration=10)
print("\nGIF salvo como evolucao.gif")

# --- GRÁFICO FINAL ---

plt.figure()
plt.plot(historico_fitness, label="Melhor")
plt.plot(historico_fitness_medio, label="Médio")
plt.title("Evolução do Fitness")
plt.xlabel("Geração")
plt.ylabel("Fitness")
plt.legend()
plt.grid(True)
plt.savefig("evolucao_fitness.png")  # salva o gráfico
plt.close()  # fecha a figura

