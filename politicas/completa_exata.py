from math import ceil

from .politica import Politica


class CompletaExataVisual(Politica):
    """
    Versão didática/visual inspirada no fluxo da política Completa Exata:

    1. Calcula Lower Bound (LB).
    2. Usa Best Fit Decreasing para obter Upper Bound (UB).
    3. Calcula somas alcançáveis com programação dinâmica por bitset.
    4. Tenta encontrar solução exata entre LB e UB.
    5. Registra eventos para a interface explicar cada etapa.
    """

    nome = "Completa Exata (Visual)"

    def ordenar_itens(self, itens):
        return sorted(itens, reverse=True)

    def calcular_lower_bound(self, itens, capacidade):
        if not itens:
            return 0
        return ceil(sum(itens) / capacidade)

    def best_fit_decreasing(self, itens, capacidade):
        caixas = []

        for item in sorted(itens, reverse=True):
            melhor = None
            menor_sobra = None

            for i, caixa in enumerate(caixas):
                usado = sum(caixa)
                if usado + item <= capacidade:
                    sobra = capacidade - (usado + item)
                    if menor_sobra is None or sobra < menor_sobra:
                        menor_sobra = sobra
                        melhor = i

            if melhor is None:
                caixas.append([item])
            else:
                caixas[melhor].append(item)

        return caixas

    def somas_alcancaveis_bitset(self, itens, limite):
        """
        bit s == 1 significa: existe algum subconjunto cuja soma é s.
        """
        bits = 1  # somente soma 0
        mascara = (1 << (limite + 1)) - 1

        for item in itens:
            bits |= (bits << item)
            bits &= mascara

        return bits

    def listar_somas(self, bits, limite):
        return [s for s in range(limite + 1) if (bits >> s) & 1]

    def _busca_k(self, itens, capacidade, k, eventos=None, limite_eventos=250):
        """
        Busca exata item a item com podas de simetria.

        Para o simulador visual, mantemos a implementação simples e legível.
        """
        itens = sorted(itens, reverse=True)
        caixas = [[] for _ in range(k)]
        cargas = [0] * k

        # Sufixos em bitset: ajuda a verificar quais somas ainda são possíveis.
        sufixos = [0] * (len(itens) + 1)
        sufixos[len(itens)] = 1
        mascara = (1 << (capacidade + 1)) - 1

        for i in range(len(itens) - 1, -1, -1):
            item = itens[i]
            r = sufixos[i + 1]
            sufixos[i] = (r | (r << item)) & mascara

        def registrar(tipo, mensagem, **extra):
            if eventos is None or len(eventos) >= limite_eventos:
                return
            eventos.append({
                "tipo": tipo,
                "mensagem": mensagem,
                "caixas": [c.copy() for c in caixas],
                "cargas": cargas.copy(),
                **extra,
            })

        def dfs(pos):
            if pos == len(itens):
                return True

            item = itens[pos]

            # Primeiro tenta as caixas mais cheias onde o item ainda cabe.
            ordem = sorted(
                range(k),
                key=lambda i: capacidade - cargas[i]
            )

            cargas_testadas = set()

            for i in ordem:
                if cargas[i] + item > capacidade:
                    continue

                # Caixas com a mesma carga são simétricas.
                if cargas[i] in cargas_testadas:
                    continue
                cargas_testadas.add(cargas[i])

                sobra_depois = capacidade - (cargas[i] + item)

                # Poda didática usando bitset:
                # se a caixa ainda tem sobra e nenhuma soma futura consegue
                # atingir exatamente essa sobra, isso NÃO prova inviabilidade
                # global; por isso usamos apenas como informação visual.
                pode_completar = bool(
                    (sufixos[pos + 1] >> sobra_depois) & 1
                ) if sobra_depois >= 0 else False

                caixas[i].append(item)
                cargas[i] += item

                registrar(
                    "busca_coloca",
                    f"Testando item {item} na Caixa {i + 1}. "
                    f"Carga: {cargas[i]}/{capacidade}.",
                    item=item,
                    caixa=i,
                    pode_completar_exato=pode_completar,
                )

                if dfs(pos + 1):
                    return True

                cargas[i] -= item
                caixas[i].pop()

                registrar(
                    "backtrack",
                    f"Backtracking: retirar item {item} da Caixa {i + 1}.",
                    item=item,
                    caixa=i,
                )

                # Se tentamos uma caixa vazia e falhou, outras vazias são equivalentes.
                if cargas[i] == 0:
                    break

            return False

        encontrou = dfs(0)
        return [c.copy() for c in caixas] if encontrou else None

    def empacotar(self, itens, capacidade, registrar_eventos=False):
        itens = list(itens)

        if not itens:
            return {
                "caixas": [],
                "lower_bound": 0,
                "upper_bound": 0,
                "otimo_comprovado": True,
                "eventos": [],
            }

        if any(item <= 0 for item in itens):
            raise ValueError("Todos os itens devem ser maiores que zero.")

        if any(item > capacidade for item in itens):
            raise ValueError("Existe item maior que a capacidade da caixa.")

        eventos = [] if registrar_eventos else None

        def evento(tipo, mensagem, **extra):
            if eventos is not None:
                eventos.append({
                    "tipo": tipo,
                    "mensagem": mensagem,
                    **extra,
                })

        itens_ord = sorted(itens, reverse=True)

        evento(
            "inicio",
            f"Itens ordenados do maior para o menor: {itens_ord}",
            itens=itens_ord,
        )

        lb = self.calcular_lower_bound(itens_ord, capacidade)
        evento(
            "lower_bound",
            f"Lower Bound = ceil({sum(itens_ord)} / {capacidade}) = {lb}. "
            f"É impossível usar menos de {lb} caixas.",
            lower_bound=lb,
        )

        bfd = self.best_fit_decreasing(itens_ord, capacidade)
        ub = len(bfd)
        evento(
            "upper_bound",
            f"O Best Fit Decreasing encontrou uma solução com {ub} caixas. "
            f"Logo, UB = {ub}.",
            upper_bound=ub,
            caixas=[c.copy() for c in bfd],
        )

        bits = self.somas_alcancaveis_bitset(itens_ord, capacidade)
        somas = self.listar_somas(bits, capacidade)
        evento(
            "bitset",
            "Programação dinâmica por bitset calculou as somas de itens "
            f"alcançáveis até a capacidade {capacidade}.",
            somas=somas,
        )

        if lb == ub:
            evento(
                "otimo",
                f"LB = UB = {lb}. A solução do BFD já é ótima.",
                caixas=[c.copy() for c in bfd],
            )
            return {
                "caixas": bfd,
                "lower_bound": lb,
                "upper_bound": ub,
                "otimo_comprovado": True,
                "eventos": eventos or [],
            }

        melhor = bfd

        for k in range(lb, ub):
            evento(
                "tentativa_k",
                f"Busca exata: tentando empacotar todos os itens em {k} caixas.",
                k=k,
            )

            solucao = self._busca_k(
                itens_ord,
                capacidade,
                k,
                eventos=eventos,
            )

            if solucao is not None:
                melhor = solucao
                evento(
                    "solucao_k",
                    f"Encontrada solução com {k} caixas.",
                    k=k,
                    caixas=[c.copy() for c in solucao],
                )

                # Como começamos no LB e subimos, a primeira solução é ótima.
                return {
                    "caixas": melhor,
                    "lower_bound": lb,
                    "upper_bound": ub,
                    "otimo_comprovado": k == lb,
                    "eventos": eventos or [],
                }

            evento(
                "falha_k",
                f"Não foi encontrada solução com {k} caixas.",
                k=k,
            )

        return {
            "caixas": melhor,
            "lower_bound": lb,
            "upper_bound": ub,
            "otimo_comprovado": len(melhor) == lb,
            "eventos": eventos or [],
        }
