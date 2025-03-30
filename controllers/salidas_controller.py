from flask import Blueprint, request, jsonify, current_app
from db import get_connection
import os
from datetime import datetime
from werkzeug.utils import secure_filename

salidas_bp = Blueprint('salidas', __name__)
UPLOAD_FOLDER = 'uploads'  # Asegúrate de tener esta carpeta configurada en app.config

@salidas_bp.route('/', methods=['POST'])
def crear_salida():
    tipo = request.form['tipo']
    monto = request.form['monto']
    fecha = request.form['fecha']
    usuario_id = request.form['usuario_id']
    cantidad = int(request.form.get('cantidad', 1))

    factura = request.files.get('factura')
    factura_filename = None

    if factura:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        factura_filename = f"{timestamp}_{secure_filename(factura.filename)}"
        factura.save(os.path.join(current_app.config['UPLOAD_FOLDER'], factura_filename))

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO salidas (usuario_id, tipo, monto, fecha, factura_ruta, cantidad)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (usuario_id, tipo, monto, fecha, factura_filename, cantidad))
        conn.commit()

    conn.close()
    return jsonify({"success": True})


@salidas_bp.route('/<int:usuario_id>', methods=['GET'])
def listar_salidas(usuario_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM salidas WHERE usuario_id = %s", (usuario_id,))
        salidas = cursor.fetchall()
    conn.close()
    return jsonify(salidas)

@salidas_bp.route('/update/<int:id>', methods=['PUT'])
def actualizar_salida(id):
    tipo = request.form['tipo']
    monto = request.form['monto']
    fecha = request.form['fecha']
    cantidad = int(request.form.get('cantidad', 1))
    usuario_id = request.form['usuario_id']
    rol = request.form.get('rol')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT usuario_id FROM salidas WHERE id = %s", (id,))
        salida = cursor.fetchone()
        if not salida:
            return jsonify({"success": False, "message": "Salida no encontrada"}), 404
        if rol != "admin" and str(salida['usuario_id']) != str(usuario_id):
            return jsonify({"success": False, "message": "No autorizado"}), 403

        cursor.execute("""
            UPDATE salidas
            SET tipo = %s, monto = %s, fecha = %s, cantidad = %s
            WHERE id = %s
        """, (tipo, monto, fecha, cantidad, id))
        conn.commit()

    conn.close()
    return jsonify({"success": True})


@salidas_bp.route('/delete/<int:id>', methods=['DELETE'])
def eliminar_salida(id):
    usuario_id = request.args.get("usuario_id")
    rol = request.args.get("rol")

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT usuario_id FROM salidas WHERE id = %s", (id,))
        salida = cursor.fetchone()
        if not salida:
            return jsonify({"success": False, "message": "Salida no encontrada"}), 404
        if rol != "admin" and str(salida['usuario_id']) != str(usuario_id):
            return jsonify({"success": False, "message": "No autorizado"}), 403

        cursor.execute("DELETE FROM salidas WHERE id = %s", (id,))
        conn.commit()

    conn.close()
    return jsonify({"success": True})

