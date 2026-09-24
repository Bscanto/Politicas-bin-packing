def gerar_passos(itens, capacidade, politica):

    # Política completa/exata: ela precisa enxergar todos os itens ao mesmo tempo.
    if hasattr(politica, "empacotar"):
        dados = politica.empacotar(
            itens,
            capacidade,
            registrar_eventos=True
        )

        passos = []
        ultimas_caixas = []

        for evento in dados["eventos"]:
            caixas = evento.get("caixas", ultimas_caixas)
            if caixas:
                ultimas_caixas = [c.copy() for c in caixas]

            passos.append({
                "tipo": evento["tipo"],
                "item": evento.get("item"),
                "caixas": [c.copy() for c in caixas],
                "caixa_analisada": evento.get("caixa"),
                "mensagem": evento["mensagem"],
                "lower_bound": evento.get(
                    "lower_bound",
                    dados.get("lower_bound")
                ),
                "upper_bound": evento.get(
                    "upper_bound",
                    dados.get("upper_bound")
                ),
                "somas": evento.get("somas"),
                "k": evento.get("k"),
                "pode_completar_exato": evento.get(
                    "pode_completar_exato"
                ),
            })

        passos.append({
            "tipo": "final",
            "item": None,
            "caixas": [
                caixa.copy()
                for caixa in dados["caixas"]
            ],
            "mensagem": (
                f"Simulação finalizada. "
                f"{len(dados['caixas'])} caixas utilizadas. "
                f"Ótimo comprovado: "
                f"{'sim' if dados.get('otimo_comprovado') else 'não'}."
            ),
            "lower_bound": dados.get("lower_bound"),
            "upper_bound": dados.get("upper_bound"),
            "somas": None,
            "k": len(dados["caixas"]),
            "pode_completar_exato": None,
        })

        return passos

    # Políticas heurísticas tradicionais: execução item a item.
    itens_processados = politica.ordenar_itens(itens)
    caixas = []
    passos = []

    passos.append({
        "tipo": "ordenacao",
        "item": None,
        "caixas": [],
        "mensagem": (
            f"Itens utilizados pela política: "
            f"{itens_processados}"
        )
    })

    for item in itens_processados:
        indice_caixa = politica.escolher_caixa(
            item,
            caixas,
            capacidade
        )

        if caixas:
            for indice, caixa in enumerate(caixas):
                total = sum(caixa)
                novo_total = total + item
                cabe = novo_total <= capacidade

                mensagem = (
                    f"Caixa {indice + 1}: "
                    f"{total} + {item} = {novo_total}. "
                    f"O item {'cabe' if cabe else 'não cabe'}."
                )

                passos.append({
                    "tipo": "tentativa",
                    "item": item,
                    "caixas": [
                        caixa.copy()
                        for caixa in caixas
                    ],
                    "caixa_analisada": indice,
                    "mensagem": mensagem
                })

        if indice_caixa is not None:
            caixas[indice_caixa].append(item)

            passos.append({
                "tipo": "colocado",
                "item": item,
                "caixas": [
                    caixa.copy()
                    for caixa in caixas
                ],
                "caixa_analisada": indice_caixa,
                "mensagem": (
                    f"Item {item} colocado na "
                    f"Caixa {indice_caixa + 1}."
                )
            })
        else:
            caixas.append([item])

            passos.append({
                "tipo": "nova_caixa",
                "item": item,
                "caixas": [
                    caixa.copy()
                    for caixa in caixas
                ],
                "mensagem": (
                    f"Item {item} não cabe nas "
                    f"caixas existentes. Nova caixa criada."
                )
            })

    passos.append({
        "tipo": "final",
        "item": None,
        "caixas": [
            caixa.copy()
            for caixa in caixas
        ],
        "mensagem": (
            f"Simulação finalizada. "
            f"{len(caixas)} caixas utilizadas."
        )
    })

    return passos
