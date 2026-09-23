from .politica import Politica


class BestFit(Politica):

    def escolher_caixa(self, item, caixas, capacidade):

        melhor_caixa = None
        menor_espaco_restante = None

        for indice, caixa in enumerate(caixas):

            total = sum(caixa)

            if total + item <= capacidade:

                espaco_restante = capacidade - (
                    total + item
                )

                if (
                    menor_espaco_restante is None
                    or espaco_restante < menor_espaco_restante
                ):

                    menor_espaco_restante = espaco_restante
                    melhor_caixa = indice

        return melhor_caixa