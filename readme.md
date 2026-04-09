# 🧬 Algoritmo Genético: Otimização da Função Schaffer's f6

Este projeto implementa um **Algoritmo Genético (AG)** para encontrar o valor máximo da função **Schaffer's f6**, um problema clássico de otimização multidimensional conhecido por sua superfície complexa e pela presença de diversos ótimos locais.

---

## 🛠️ Justificativa dos Parâmetros e Funções

### 1. Representação do Cromossomo (Real)

Optamos pela **representação real** em vez da binária.

**Por quê?**  
Segundo os slides da disciplina (pág. 26–28), a representação real é ideal para otimização de funções contínuas. Ela evita o erro de discretização e permite que os genes (`x`, `y`) sejam manipulados diretamente na escala do problema, garantindo maior precisão decimal.

---

### 2. Função de Aptidão (Fitness)

A função de fitness utilizada é a própria **Schaffer's f6**.

**A dificuldade dela:**  
Ela possui um único pico global de valor `1.0` em `(0,0)`, mas é cercada por infinitos "anéis" (ótimos locais), que podem aprisionar algoritmos menos robustos.

---

### 3. Seleção por Torneio (`k = 3`)

**Por quê?**  
Diferente da roleta, o torneio mantém uma pressão seletiva constante e não depende da soma total dos fitness da população. (definição dos slides)

Ao escolher 3 indivíduos aleatórios e selecionar o melhor:
- Indivíduos bons têm alta chance de reprodução
- Indivíduos menos aptos ainda podem sobreviver ocasionalmente

Isso ajuda a manter a diversidade da população.

---

### 4. Recombinação (Crossover Aritmético)

Utilizamos média ponderada entre os genes dos pais (`α = 0.5`). - crossover aritmético

**Por quê?**  
Para cromossomos reais, isso garante que o filho esteja exatamente no espaço geométrico entre os pais, refinando a busca em direção ao ótimo.

---

### 5. Mutação Gaussiana (`σ = 5`)

Aplicamos um deslocamento baseado em uma distribuição normal.

**Por quê?**  
A mutação é o principal mecanismo de **exploração**:
- Pequenos ajustes finos na maioria das vezes
- Possibilidade de saltos maiores para escapar dos ótimos locais, como explicado

---

### 6. Elitismo (`n = 2`)

**Por quê?**  
Evita que as melhores soluções sejam perdidas durante as operações genéticas.

Garantir a sobrevivência dos 2 melhores indivíduos faz com que o fitness da população seja **monótono não-decrescente**.

---

### 7. Espaço de Busca (`[-100, 100]`)

**Por quê?**  
Um domínio amplo testa a capacidade do algoritmo de localizar uma região extremamente pequena (o ótimo global em `(0,0)`), demonstrando eficiência de busca global. - ao testar com um espaço de busca pequeno, podemos alcançar um resultado prematuro com alto fit e ficar preso em um ótimo local sem conseguir sair

---

## 📈 Como avaliar os resultados

### 🔹 1. Valor do Melhor Fitness

- **Excelente:** próximo de `1.0000` (ex: `0.9903+`)
- **Regular:** entre `0.80` e `0.95`
  - Indica possível aprisionamento em ótimo local
  - Sugestão: aumentar taxa de mutação

---

### 🔹 2. Gráfico de Convergência

- Deve subir rapidamente nas primeiras gerações
- Depois estabilizar próximo do valor máximo

⚠️ Se a linha estiver reta desde o início:
- Espaço de busca pode estar pequeno demais
- População pode estar pouco diversa

---

### 🔹 3. Distribuição Espacial (Gráfico de Dispersão)

- **Início:** pontos espalhados
- **Final:** pontos concentrados em `(0,0)`

⚠️ Se ainda houver dispersão no final:
- O algoritmo não convergiu adequadamente

---

## 🚀 Como rodar o projeto

### 1. Instale as dependências

```bash
Certifique-se de ter numpy e matplotlib instalados.

Execute python alg_genetico.py.

Confira os frames gerados na pasta /frames.