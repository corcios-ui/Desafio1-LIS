class Salida:
    def __init__(self, id, usuario_id, tipo, monto, fecha, factura_ruta, cantidad):
        self.id = id
        self.usuario_id = usuario_id
        self.tipo = tipo
        self.monto = monto
        self.fecha = fecha
        self.factura_ruta = factura_ruta
        self.cantidad = cantidad

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "tipo": self.tipo,
            "monto": float(self.monto),
            "fecha": self.fecha.strftime("%Y-%m-%d") if self.fecha else None,
            "factura_ruta": self.factura_ruta,
            "cantidad": self.cantidad
        }
