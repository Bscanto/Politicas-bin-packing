class Politica:

    def escolher_caixa(self, item, caixas, capacidade):
        raise NotImplementedError(
            "A política deve implementar escolher_caixa()."
        )

    def ordenar_itens(self, itens):
        return itens