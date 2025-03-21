from flask import Blueprint, jsonify
from db import get_connection

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/api/productos', methods=['GET'])
def listar_productos():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
    conn.close()
    return jsonify(productos)
