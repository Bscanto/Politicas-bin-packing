# Torneio de Políticas de Bin Packing

Projeto desenvolvido no contexto do Mestrado em Computação para estudo, simulação e comparação de políticas de empacotamento de itens (Bin Packing).

## Objetivo

O projeto tem como objetivo implementar e comparar diferentes políticas heurísticas para o problema de Bin Packing, permitindo analisar seu comportamento em diferentes conjuntos de itens.

As políticas inicialmente implementadas são:

- First Fit (FF)
- First Fit Decreasing (FFD)
- Best Fit (BF)

## Problema de Bin Packing

O problema de Bin Packing consiste em distribuir um conjunto de itens em recipientes (bins/caixas) de capacidade limitada, buscando utilizar a menor quantidade possível de recipientes.

Cada item possui um determinado tamanho e cada caixa possui uma capacidade máxima.

## Políticas implementadas

### First Fit

Percorre as caixas existentes e coloca o item na primeira caixa em que ele couber.

### First Fit Decreasing

Ordena os itens em ordem decrescente e aplica a estratégia First Fit.

### Best Fit

Coloca o item na caixa que resulte no menor espaço residual possível, desde que o item caiba.

## Métricas

O sistema permite comparar as políticas utilizando:

- Número de caixas utilizadas;
- Utilização das caixas;
- Desperdício de capacidade;
- Tempo de execução.

## Interface

O projeto possui uma interface desenvolvida com Streamlit que permite visualizar a execução das políticas e comparar seus resultados.

## Tecnologias

- Python
- Streamlit
- Git
- GitHub

## Execução

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd Politicas_Bin_Packing
```


Execute a aplicação:

```bash
streamlit run app.py
```
