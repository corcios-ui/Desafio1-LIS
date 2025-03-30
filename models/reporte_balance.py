class ReporteBalance:
    def __init__(self, entradas, salidas):
        self.entradas = entradas
        self.salidas = salidas

    def total_entradas(self):
        return sum([e.monto for e in self.entradas])

    def total_salidas(self):
        return sum([s.monto for s in self.salidas])

    def balance(self):
        return self.total_entradas() - self.total_salidas()

    def generar_reporte_dict(self):
        return {
            "total_entradas": self.total_entradas(),
            "total_salidas": self.total_salidas(),
            "balance": self.balance()
        }
