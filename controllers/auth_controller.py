from flask import Blueprint, request, jsonify
from db import get_connection

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password_hash=%s", (username, password))
        user = cursor.fetchone()

    conn.close()

    if user:
        return jsonify({
            "success": True,
            "user_id": user['id'],
            "rol": user['rol']
        })
    else:
        return jsonify({"success": False, "message": "Usuario o contraseña incorrectos"}), 401


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    rol = data.get('rol', 'empleado')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM usuarios WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "El usuario ya existe"}), 400

        cursor.execute("INSERT INTO usuarios (username, password_hash, rol) VALUES (%s, %s, %s)",
                       (username, password, rol))
        conn.commit()
        return jsonify({"success": True, "message": "Usuario creado con éxito"})
