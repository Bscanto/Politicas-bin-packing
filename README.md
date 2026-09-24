# 📦 Simulador Visual de Políticas de Bin Packing

Projeto desenvolvido no contexto do Mestrado em Computação para estudo, simulação e comparação de políticas de empacotamento de itens no problema de **Bin Packing**.

Além das heurísticas clássicas, o projeto inclui uma política **Completa Exata (Visual)** inspirada no fluxo da política `group_xx.py`, permitindo visualizar conceitos como **Lower Bound (LB)**, **Upper Bound (UB)**, **Best Fit Decreasing**, **programação dinâmica com bitsets**, **busca exata** e **backtracking**.

---

## 🎯 Objetivo

O objetivo do projeto é comparar diferentes estratégias para o problema de Bin Packing e, ao mesmo tempo, tornar visual o funcionamento interno dos algoritmos.

O sistema permite observar:

- como os itens são distribuídos entre as caixas;
- quantas caixas cada política utiliza;
- a taxa de utilização;
- o desperdício de capacidade;
- o tempo de execução;
- o Lower Bound e o Upper Bound da política Completa Exata;
- as somas alcançáveis calculadas com bitsets;
- as tentativas realizadas durante a busca exata;
- os momentos em que ocorre backtracking;
- quando uma solução ótima é comprovada.

---

## 🧩 Problema de Bin Packing

O problema de **Bin Packing** consiste em distribuir um conjunto de itens em caixas de capacidade limitada, buscando utilizar a menor quantidade possível de caixas.

Neste simulador, todas as caixas possuem a mesma capacidade.

Exemplo:

```text
Capacidade de cada caixa: 10
Itens: [2, 5, 7, 8, 3, 4, 6, 1, 9, 5]
```

A meta é distribuir todos os itens sem ultrapassar a capacidade de nenhuma caixa e tentando minimizar a quantidade total utilizada.

---

## 🧠 Políticas implementadas

### First Fit (FF)

Percorre as caixas existentes e coloca cada item na primeira caixa em que ele couber.

### First Fit Decreasing (FFD)

Ordena os itens do maior para o menor e depois aplica First Fit.

### Best Fit (BF)

Para cada item, procura a caixa que deixe o menor espaço residual possível depois da inserção.

### Completa Exata (Visual)

A política **Completa Exata (Visual)** segue um fluxo inspirado na política, adaptado para o simulador.

Fluxo geral:

```text
Itens
  ↓
Ordenação decrescente
  ↓
Lower Bound (LB)
  ↓
Best Fit Decreasing
  ↓
Upper Bound (UB)
  ↓
Programação dinâmica com bitsets
  ↓
Busca exata entre LB e UB
  ↓
Backtracking
  ↓
Melhor solução encontrada
```

---

## 1. Lower Bound — LB

O **Lower Bound** representa o menor número teórico de caixas necessárias.

No simulador:

```text
LB = ceil(soma dos itens / capacidade da caixa)
```

Exemplo:

```text
Soma dos itens = 50
Capacidade = 10

LB = ceil(50 / 10)
LB = 5
```

Isso significa que é impossível utilizar menos de 5 caixas.

Se a política encontrar uma solução com exatamente 5 caixas, essa solução é ótima.

---

## 2. Upper Bound — UB

Depois de calcular o LB, a política executa **Best Fit Decreasing (BFD)**.

O número de caixas encontrado pelo BFD é usado como **Upper Bound**.

Exemplo:

```text
LB = 5

BFD encontrou solução com 7 caixas.

UB = 7
```

Logo:

```text
5 ≤ ótimo ≤ 7
```

---

## 3. Programação dinâmica com bitsets

A política utiliza programação dinâmica para calcular quais somas podem ser formadas com os itens disponíveis.

Exemplo com:

```text
[2, 9, 10]
```

Temos:

```text
início
{0}

+ item 2
{0, 2}

+ item 9
{0, 2, 9, 11}

+ item 10
{0, 2, 9, 10, 11, 12, 19, 21}
```

Assim, a política consegue saber rapidamente se determinado volume pode ser formado pelos itens restantes.

Exemplo:

```text
19 → possível
21 → possível
20 → não é possível
```

Essas informações ajudam a orientar a busca e evitar tentativas desnecessárias.

---

## 4. Busca exata

Quando o Lower Bound e o Upper Bound são diferentes, a política tenta encontrar uma solução melhor.

Exemplo:

```text
LB = 5
UB = 7
```

A busca tenta encontrar uma solução começando pelo menor valor possível.

```text
K = 5
K = 6
```

Se uma solução for encontrada com:

```text
K = LB
```

o ótimo está comprovado.

---

## 5. Backtracking

Durante a busca exata, o algoritmo testa diferentes combinações.

Quando uma escolha leva a um caminho que não consegue empacotar todos os itens, a política volta para uma decisão anterior.

Esse processo é chamado de **backtracking**.

A interface mostra visualmente eventos como:

```text
Testando item 9 na Caixa 1
Testando item 8 na Caixa 2
Testando item 7 na Caixa 3

Backtracking:
retirar item 7 da Caixa 3
```

---

## 🖥️ Interface visual

A aplicação foi desenvolvida com **Streamlit**.

Na política Completa Exata (Visual), a interface apresenta:

- etapa atual do algoritmo;
- item atualmente analisado;
- caixas e seus conteúdos;
- ocupação de cada caixa;
- espaço restante;
- Lower Bound;
- Upper Bound;
- valor de K atualmente testado;
- somas alcançáveis;
- eventos da busca exata;
- backtracking;
- solução final.

É possível navegar passo a passo usando:

```text
◀ Anterior
Próximo ▶
🔄 Reiniciar
```

---

## 📊 Comparação das políticas

O simulador permite comparar:

- First Fit;
- First Fit Decreasing;
- Best Fit;
- Completa Exata.

As métricas apresentadas são:

| Métrica | Descrição |
|---|---|
| Caixas | Número de caixas utilizadas |
| Utilização | Percentual de capacidade aproveitada |
| Desperdício | Espaço total não utilizado |
| Tempo | Tempo de execução em milissegundos |
| LB | Lower Bound, quando disponível |
| UB | Upper Bound, quando disponível |
| Ótimo comprovado | Indica se a solução atingiu o Lower Bound |

---

## 📁 Estrutura do projeto

```text
Politicas-bin-packing/
│
├── app.py
├── README.md
│
├── politicas/
│   ├── __init__.py
│   ├── politica.py
│   ├── first_fit.py
│   ├── first_fit_decreasing.py
│   ├── best_fit.py
│   └── completa_exata.py
│
└── utils/
    ├── __init__.py
    ├── avaliacao.py
    └── simulacao.py
```

---

## ▶️ Como executar

Clone o repositório:

```bash
git clone https://github.com/Bscanto/Politicas-bin-packing.git
```

Entre na pasta:

```bash
cd Politicas-bin-packing
```

Instale o Streamlit, caso ainda não tenha:

```bash
pip install streamlit
```

Execute a aplicação:

```bash
streamlit run app.py
```

---

## 🧪 Exemplo de uso

Na barra lateral da aplicação:

```text
Política: Completa Exata (Visual)
Capacidade: 10
Itens: 2, 5, 7, 8, 3, 4, 6, 1, 9, 5
```

Clique em:

```text
▶ Iniciar simulação
```

para acompanhar a execução passo a passo.

Use:

```text
📊 Comparar políticas
```

para comparar todas as estratégias disponíveis.

---

## 🛠️ Tecnologias

- Python
- Streamlit
- Git
- GitHub

---

## 📚 Conceitos demonstrados

O projeto permite estudar de forma prática:

- Bin Packing Problem;
- algoritmos gulosos;
- First Fit;
- First Fit Decreasing;
- Best Fit;
- Lower Bound;
- Upper Bound;
- programação dinâmica;
- bitsets;
- busca em profundidade;
- backtracking;
- comparação de heurísticas;
- análise de desempenho.
