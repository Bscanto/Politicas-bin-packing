from .politica import Politica


class FirstFit(Politica):

    def escolher_caixa(self, item, caixas, capacidade):

        for indice, caixa in enumerate(caixas):

            if sum(caixa) + item <= capacidade:
                return indice

        return None