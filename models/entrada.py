class Entrada:
    def __init__(self, id, usuario_id, tipo, monto, fecha, factura_ruta, imagen_articulo, cantidad, producto_id=None):
        self.id = id
        self.usuario_id = usuario_id
        self.tipo = tipo
        self.monto = monto
        self.fecha = fecha
        self.factura_ruta = factura_ruta
        self.imagen_articulo = imagen_articulo
        self.cantidad = cantidad
        self.producto_id = producto_id

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "tipo": self.tipo,
            "monto": float(self.monto),
            "fecha": self.fecha.strftime("%Y-%m-%d") if self.fecha else None,
            "factura_ruta": self.factura_ruta,
            "imagen_articulo": self.imagen_articulo,
            "cantidad": self.cantidad,
            "producto_id": self.producto_id
        }
