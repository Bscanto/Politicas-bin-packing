from .first_fit import FirstFit


class FirstFitDecreasing(FirstFit):

    def ordenar_itens(self, itens):

        return sorted(
            itens,
            reverse=True
        )