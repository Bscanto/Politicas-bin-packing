import time


def executar_politica(itens, capacidade, politica):
    """Executa uma política e calcula métricas."""

    inicio = time.perf_counter()

    if hasattr(politica, "empacotar"):
        dados = politica.empacotar(
            itens,
            capacidade,
            registrar_eventos=False
        )
        caixas = dados["caixas"]
        lower_bound = dados.get("lower_bound")
        upper_bound = dados.get("upper_bound")
        otimo_comprovado = dados.get("otimo_comprovado", False)
    else:
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

        lower_bound = None
        upper_bound = None
        otimo_comprovado = False

    fim = time.perf_counter()
    tempo = (fim - inicio) * 1000

    numero_caixas = len(caixas)
    capacidade_total = numero_caixas * capacidade
    total_utilizado = sum(sum(caixa) for caixa in caixas)
    desperdicio = capacidade_total - total_utilizado

    utilizacao = (
        total_utilizado / capacidade_total * 100
        if capacidade_total > 0
        else 0
    )

    return {
        "caixas": caixas,
        "numero_caixas": numero_caixas,
        "capacidade_total": capacidade_total,
        "total_utilizado": total_utilizado,
        "utilizacao": utilizacao,
        "desperdicio": desperdicio,
        "tempo": tempo,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "otimo_comprovado": otimo_comprovado,
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
