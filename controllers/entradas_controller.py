from flask import Blueprint, request, jsonify, current_app
from db import get_connection
import os

entradas_bp = Blueprint('entradas', __name__)

@entradas_bp.route('/', methods=['POST'])
def crear_entrada():
    tipo = request.form['tipo']  # nombre del producto
    monto = request.form['monto']
    fecha = request.form['fecha']
    usuario_id = request.form['usuario_id']
    cantidad = int(request.form.get('cantidad', 1))

    factura = request.files.get('factura')
    imagen = request.files.get('imagen')

    factura_filename = f"{usuario_id}_{factura.filename}" if factura else None
    imagen_filename = f"{usuario_id}_{imagen.filename}" if imagen else None

    if factura:
        factura.save(os.path.join(current_app.config['UPLOAD_FOLDER'], factura_filename))
    if imagen:
        imagen.save(os.path.join(current_app.config['UPLOAD_FOLDER'], imagen_filename))

    conn = get_connection()
    with conn.cursor() as cursor:
        # Verificar si el producto ya existe
        cursor.execute("SELECT id FROM productos WHERE nombre = %s", (tipo,))
        producto = cursor.fetchone()

        if producto:
            producto_id = producto['id']
            cursor.execute("UPDATE productos SET cantidad = cantidad + %s WHERE id = %s", (cantidad, producto_id))
        else:
            cursor.execute("""
                INSERT INTO productos (nombre, precio, cantidad, detalles, imagen)
                VALUES (%s, %s, %s, %s, %s)
            """, (tipo, monto, cantidad, 'Agregado desde entrada', imagen_filename))
            producto_id = cursor.lastrowid

        # Insertar entrada con referencia al producto
        cursor.execute("""
            INSERT INTO entradas (usuario_id, tipo, monto, fecha, factura_ruta, imagen_articulo, cantidad, producto_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (usuario_id, tipo, monto, fecha, factura_filename, imagen_filename, cantidad, producto_id))

        conn.commit()

    conn.close()
    return jsonify({"success": True})

@entradas_bp.route('/<int:usuario_id>', methods=['GET'])
def listar_entradas(usuario_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM entradas WHERE usuario_id = %s", (usuario_id,))
        entradas = cursor.fetchall()
    conn.close()
    return jsonify(entradas)

@entradas_bp.route('/update/<int:id>', methods=['PUT'])
def actualizar_entrada(id):
    data = request.form
    tipo = data.get('tipo')
    monto = data.get('monto')
    fecha = data.get('fecha')
    cantidad = data.get('cantidad', 1)
    user_id = data.get('usuario_id')
    rol = data.get('rol')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT usuario_id FROM entradas WHERE id = %s", (id,))
        entrada = cursor.fetchone()
        if not entrada:
            return jsonify({"success": False, "message": "Entrada no encontrada"}), 404
        if rol != "admin" and str(entrada['usuario_id']) != str(user_id):
            return jsonify({"success": False, "message": "No autorizado"}), 403

        cursor.execute("""
            UPDATE entradas SET tipo=%s, monto=%s, fecha=%s, cantidad=%s
            WHERE id=%s
        """, (tipo, monto, fecha, cantidad, id))
        conn.commit()

    conn.close()
    return jsonify({"success": True, "message": "Entrada actualizada"})

@entradas_bp.route('/delete/<int:id>', methods=['DELETE'])
def eliminar_entrada(id):
    user_id = request.args.get('usuario_id')
    rol = request.args.get('rol')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT usuario_id FROM entradas WHERE id = %s", (id,))
        entrada = cursor.fetchone()
        if not entrada:
            return jsonify({"success": False, "message": "Entrada no encontrada"}), 404
        if rol != "admin" and str(entrada['usuario_id']) != str(user_id):
            return jsonify({"success": False, "message": "No autorizado"}), 403

        cursor.execute("DELETE FROM entradas WHERE id = %s", (id,))
        conn.commit()

    conn.close()
    return jsonify({"success": True, "message": "Entrada eliminada"})
