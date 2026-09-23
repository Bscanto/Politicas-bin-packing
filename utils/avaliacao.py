import time


def executar_politica(itens, capacidade, politica):
    """
    Executa uma política de empacotamento
    e calcula suas principais métricas.
    """

    inicio = time.perf_counter()

    itens_processados = politica.ordenar_itens(itens)

    caixas = []

    for item in itens_processados:

        indice_caixa = politica.escolher_caixa(
            item,
            caixas,
            capacidade
        )

        if indice_caixa is not None:

            caixas[indice_caixa].append(item)

        else:

            caixas.append([item])

    fim = time.perf_counter()

    tempo = (fim - inicio) * 1000

    numero_caixas = len(caixas)

    capacidade_total = numero_caixas * capacidade

    total_utilizado = sum(
        sum(caixa)
        for caixa in caixas
    )

    desperdicio = (
        capacidade_total
        - total_utilizado
    )

    if capacidade_total > 0:

        utilizacao = (
            total_utilizado
            / capacidade_total
            * 100
        )

    else:

        utilizacao = 0

    return {
        "caixas": caixas,
        "numero_caixas": numero_caixas,
        "capacidade_total": capacidade_total,
        "total_utilizado": total_utilizado,
        "utilizacao": utilizacao,
        "desperdicio": desperdicio,
        "tempo": tempo
    }
    
    
    def comparar_politicas(itens, capacidade, politicas):

      resultados = []

    for nome, politica in politicas.items():

        resultado = executar_politica(
            itens,
            capacidade,
            politica
        )

        resultado["politica"] = nome

        resultados.append(resultado)

    return resultados
  
  
def comparar_politicas(itens, capacidade, politicas):

    resultados = []

    for nome, politica in politicas.items():

        resultado = executar_politica(
            itens,
            capacidade,
            politica
        )

        resultado["politica"] = nome

        resultados.append(resultado)

    return resultados
  
if __name__ == "__main__":

    from politicas.first_fit import FirstFit
    from politicas.first_fit_decreasing import FirstFitDecreasing
    from politicas.best_fit import BestFit

    itens = [
        2, 5, 7, 8, 3,
        4, 6, 1, 9, 5
    ]

    capacidade = 10

    politicas = {
        "First Fit": FirstFit(),
        "First Fit Decreasing": FirstFitDecreasing(),
        "Best Fit": BestFit()
    }

    resultados = comparar_politicas(
        itens,
        capacidade,
        politicas
    )

    for resultado in resultados:

        print(
            resultado["politica"],
            "->",
            resultado["numero_caixas"],
            "caixas |",
            f'{resultado["utilizacao"]:.2f}%',
            "utilização |",
            resultado["desperdicio"],
            "desperdício"
        )