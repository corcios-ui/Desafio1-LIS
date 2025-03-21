import requests

BASE_URL = "http://127.0.0.1:5000/api"

def login(username, password):
    url = f"{BASE_URL}/auth/login"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    print("Login:", response.json())
    return response.json().get("user_id")

def crear_entrada(usuario_id, tipo, monto, fecha, factura_path):
    url = f"{BASE_URL}/entradas/"
    with open(factura_path, 'rb') as factura_file:
        files = {'factura': factura_file}
        data = {
            "usuario_id": usuario_id,
            "tipo": tipo,
            "monto": monto,
            "fecha": fecha
        }
        response = requests.post(url, files=files, data=data)
    print("Crear entrada:", response.json())

def listar_entradas(usuario_id):
    url = f"{BASE_URL}/entradas/{usuario_id}"
    response = requests.get(url)
    print("Entradas:", response.json())

def crear_salida(usuario_id, tipo, monto, fecha, factura_path):
    url = f"{BASE_URL}/salidas/"
    with open(factura_path, 'rb') as factura_file:
        files = {'factura': factura_file}
        data = {
            "usuario_id": usuario_id,
            "tipo": tipo,
            "monto": monto,
            "fecha": fecha
        }
        response = requests.post(url, files=files, data=data)
    print("Crear salida:", response.json())

def listar_salidas(usuario_id):
    url = f"{BASE_URL}/salidas/{usuario_id}"
    response = requests.get(url)
    print("Salidas:", response.json())

def ver_balance(usuario_id):
    url = f"{BASE_URL}/reportes/balance/{usuario_id}"
    response = requests.get(url)
    print("Balance:", response.json())

def registrar_usuario(username, password):
    url = f"{BASE_URL}/auth/register"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    print("Registrar usuario:", response.json())


if __name__ == "__main__":
    # 1. Login
    user_id = login("admin", "admin123")

    username = "juan"
    password = "1234"

    # 1. Registrar nuevo usuario (solo si no existe aún)
    registrar_usuario(username, password)

    if user_id:
        # 2. Crear entrada
        crear_entrada(user_id, "venta", 150.00, "2025-03-21", "img.png")

        # 3. Listar entradas
        listar_entradas(user_id)

        # 4. Crear salida
        crear_salida(user_id, "compra", 50.00, "2025-03-21", "img.png")

        # 5. Listar salidas
        listar_salidas(user_id)

        # 6. Ver balance
        ver_balance(user_id)
    else:
        print("Login fallido. Verifica usuario y contraseña.")
