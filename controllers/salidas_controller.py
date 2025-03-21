from flask import Blueprint, request, jsonify, current_app
from db import get_connection
import os

salidas_bp = Blueprint('salidas', __name__)

@salidas_bp.route('/', methods=['POST'])
def crear_salida():
    tipo = request.form['tipo']
    monto = request.form['monto']
    fecha = request.form['fecha']
    usuario_id = request.form['usuario_id']
    cantidad = int(request.form.get('cantidad', 1))

    factura = request.files.get('factura')
    factura_filename = f"{usuario_id}_{factura.filename}" if factura else None

    if factura:
        factura.save(os.path.join(current_app.config['UPLOAD_FOLDER'], factura_filename))

    conn = get_connection()
    with conn.cursor() as cursor:
        # Si el tipo tiene un número de producto, lo extraemos
        producto_id = None
        if tipo.startswith("compra producto"):
            try:
                producto_id = int(tipo.split(" ")[-1])
            except:
                producto_id = None

        # Si se compró un producto específico, actualizar el stock
        if producto_id:
            cursor.execute("SELECT cantidad FROM productos WHERE id = %s", (producto_id,))
            producto = cursor.fetchone()

            if not producto:
                return jsonify({"success": False, "message": "Producto no encontrado"}), 404
            if producto["cantidad"] < cantidad:
                return jsonify({"success": False, "message": "Stock insuficiente"}), 400

            # Restar stock
            cursor.execute("UPDATE productos SET cantidad = cantidad - %s WHERE id = %s", (cantidad, producto_id))

        # Guardar salida
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
