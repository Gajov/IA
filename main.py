import numpy as np
import random
import matplotlib.pyplot as plt
import os
import imageio.v2 as imageio

# ================= CONFIG =================
TAMANHO_POP = 300           # número de indivíduos na população
GERACOES = 61              # número de gerações
TAXA_CROSS = 0.8           # probabilidade de crossover
TAXA_MUT = 0.5             # taxa base de mutação
MAXMUT = 2.5               # intensidade máxima da mutação (desvio padrão do gauss)
ELITESIZE = 10             # quantidade de indivíduos preservados (elitismo)
TORNEIOSIZE = 5            # tamanho do torneio
FRM = 6                    # fator de regressão da taxa de mutação

PLOT = 'off'               # ativa/desativa geração de imagens

# ==========================================

# --- FUNÇÕES ---

def criar_população(tamanho):
    # cria população inicial com valores aleatórios entre -10 e 10
    return [[random.uniform(-10, 10), random.uniform(-10, 10)] for _ in range(tamanho)]

def fitness(x, y):
    # função Schaffer F6 (problema clássico multimodal)
    temp1 = np.sin(np.sqrt(x**2 + y**2))**2 - 0.5
    temp2 = (1.0 + 0.001 * (x**2 + y**2))**2
    return 0.5 - (temp1 / temp2)

def calcula_fitness(populacao):
    # calcula fitness de todos indivíduos
    return [fitness(ind[0], ind[1]) for ind in populacao]

def calcula_fitness_medio(populacao):
    # calcula fitness médio da população
    return sum(fitness(ind[0], ind[1]) for ind in populacao) / len(populacao)

def mutar_individuos(individuo, taxa_mutacao):
    # aplica mutação gaussiana em cada gene com certa probabilidade
    if random.random() < taxa_mutacao:
        for i in range(len(individuo)):
            individuo[i] += random.gauss(0,MAXMUT)  # ruído gaussiano
            individuo[i] = max(-10, min(10, individuo[i]))  # mantém no domínio
    return individuo

def selecao_torneio(populacao, fitnesses, k=TORNEIOSIZE):
    # seleciona k indivíduos aleatórios e retorna o melhor
    selecionados = random.sample(range(len(populacao)), k)
    melhor = selecionados[0]

    for idx in selecionados:
        if fitnesses[idx] > fitnesses[melhor]:
            melhor = idx

    return populacao[melhor]

# --- CROSSOVERS ---

def crossover(p1, p2):
    # crossover aritmético (interpolação linear)
    alpha=random.uniform(0.25,0.75)
    f1 = [alpha*p1[0] + (1-alpha)*p2[0],
          alpha*p1[1] + (1-alpha)*p2[1]]

    f2 = [(1-alpha)*p1[0] + alpha*p2[0],
          (1-alpha)*p1[1] + alpha*p2[1]]

    return f1, f2


# --- PLOT ---

def plotar_geracao(populacao, geracao, pasta="frames"):
    # cria pasta se não existir
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    # cria grade do espaço de busca
    x_range = np.linspace(-10, 10, 400)
    y_range = np.linspace(-10, 10, 400)
    X, Y = np.meshgrid(x_range, y_range)
    Z = fitness(X, Y)

    # plota função de fitness como mapa de calor
    plt.figure(figsize=(10, 8))
    contorno = plt.contourf(X, Y, Z, levels=50, cmap='viridis')
    plt.colorbar(contorno)

    # plota população
    pop_x = [ind[0] for ind in populacao]
    pop_y = [ind[1] for ind in populacao]
    plt.scatter(pop_x, pop_y, color='red', edgecolors='white', s=30, label="População")

    # encontra melhor indivíduo
    fits = calcula_fitness(populacao)
    best_idx = np.argmax(fits)
    best = populacao[best_idx]

    # destaca melhor indivíduo
    plt.scatter(best[0], best[1],
                color='yellow', edgecolors='black',
                s=120, marker='*', label="Melhor")

    plt.legend()
    plt.title(f"Geração {geracao}")
    plt.xlabel("X")
    plt.ylabel("Y")

    # salva frame
    plt.savefig(f"{pasta}/geracao_{geracao:03d}.png")
    plt.close()

# --- EXECUÇÃO ---
sucs = 0  # contador de sucessos

for i in range(100):  # roda o algoritmo 100 vezes
    pg = 0  # flag de print

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

        # normaliza tempo da geração (0 → 1)
        x = g / (GERACOES - 5)

        # decaimento da mutação ao longo do tempo
        decay = (1 - x**FRM)

        # mede diversidade: diferença entre melhor e média
        delta = (melhor_f - fit_medio) / (abs(melhor_f)+0.0000001)

        # taxa de mutação adaptativa:
        # - maior quando população está homogênea
        # - menor quando está explorando bem
        TAXA_MUT_G = max(0.0,decay * (0 + (TAXA_MUT - 0) * np.exp(-1 * delta)))

        fits = calcula_fitness(populacao)
        fit_medio = calcula_fitness_medio(populacao)
        melhor_f = max(fits)

        historico_fitness.append(melhor_f)
        historico_fitness_medio.append(fit_medio)

        # gera frame do plot (opcional)
        if (g % 2 == 0 or g == GERACOES - 1) and PLOT == 'on':
             plotar_geracao(populacao, g)

        # elitismo: mantém os melhores indivíduos
        elite_idx = np.argsort(fits)[-ELITESIZE:]
        nova_pop = [populacao[i].copy() for i in elite_idx]

        # gera nova população
        while len(nova_pop) < TAMANHO_POP:
            p1 = selecao_torneio(populacao, fits)
            p2 = selecao_torneio(populacao, fits)

            # aplica crossover
            if random.random() < TAXA_CROSS:
                    f1, f2 = crossover(p1, p2)
            else:
                f1, f2 = p1.copy(), p2.copy()

            # aplica mutação
            f1 = mutar_individuos(f1,TAXA_MUT_G)
            f2 = mutar_individuos(f2, TAXA_MUT_G)

            nova_pop.append(f1)
            if len(nova_pop) < TAMANHO_POP:
                nova_pop.append(f2)

        populacao = nova_pop

        # verifica sucesso (próximo do ótimo global)
        if melhor_f>0.9904 and pg == 0:
            print(f"Geracao {g}: Melhor={melhor_f:.6f} | Medio={fit_medio:.6} | TAXAMUT={TAXA_MUT_G:.2}")
            pg = 1
        elif PLOT=='on': 
            print(f"Geracao {g}: Melhor={melhor_f:.6f} | Medio={fit_medio:.6} | TAXAMUT={TAXA_MUT_G:.2}")

    # contabiliza sucesso
    if melhor_f>0.9904:
        sucs += 1 

print(f"Taxa de sucesso: {sucs}%")

# --- GIF ---
if PLOT == 'on':
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