def gerar_passos(itens, capacidade, politica):

    # A política decide se os itens precisam ser ordenados
    itens_processados = politica.ordenar_itens(itens)

    caixas = []

    passos = []

    # ========================================================
    # ORDENAÇÃO
    # ========================================================

    passos.append({
        "tipo": "ordenacao",
        "item": None,
        "caixas": [],
        "mensagem": (
            f"Itens utilizados pela política: "
            f"{itens_processados}"
        )
    })

    # ========================================================
    # PROCESSAMENTO
    # ========================================================

    for item in itens_processados:

        # A política decide onde colocar
        indice_caixa = politica.escolher_caixa(
            item,
            caixas,
            capacidade
        )

        # ====================================================
        # TENTATIVAS
        # ====================================================

        if caixas:

            for indice, caixa in enumerate(caixas):

                total = sum(caixa)

                novo_total = total + item

                cabe = novo_total <= capacidade

                if cabe:

                    mensagem = (
                        f"Caixa {indice + 1}: "
                        f"{total} + {item} = {novo_total}. "
                        f"O item cabe."
                    )

                else:

                    mensagem = (
                        f"Caixa {indice + 1}: "
                        f"{total} + {item} = {novo_total}. "
                        f"O item não cabe."
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

        # ====================================================
        # COLOCA ITEM
        # ====================================================

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

        # ====================================================
        # NOVA CAIXA
        # ====================================================

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
                    f"caixas existentes. "
                    f"Nova caixa criada."
                )
            })

    # ========================================================
    # FINAL
    # ========================================================

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