class Usuario:
    def __init__(self, id, username, rol):
        self.id = id
        self.username = username
        self.rol = rol

    def es_admin(self):
        return self.rol == 'admin'

    def es_empleado(self):
        return self.rol == 'empleado'
