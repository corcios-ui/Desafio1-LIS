from flask import Blueprint, request, jsonify
from db import get_connection

reportes_bp = Blueprint('reportes', __name__)


@reportes_bp.route('/balance/<int:usuario_id>', methods=['GET'])
def balance(usuario_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT SUM(monto) as total_entradas FROM entradas WHERE usuario_id = %s", (usuario_id,))
        total_entradas = cursor.fetchone()['total_entradas'] or 0

        cursor.execute("SELECT SUM(monto) as total_salidas FROM salidas WHERE usuario_id = %s", (usuario_id,))
        total_salidas = cursor.fetchone()['total_salidas'] or 0

    conn.close()
    balance = total_entradas - total_salidas
    return jsonify({
        "entradas": total_entradas,
        "salidas": total_salidas,
        "balance": balance
    })
