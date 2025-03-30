from flask import Blueprint, request, jsonify
from db import get_connection
from flask import send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

reportes_bp = Blueprint('reportes_bp', __name__)


@reportes_bp.route('/balance')
def balance_mensual():
    usuario_id = request.args.get('usuario_id')
    inicio = request.args.get('inicio')
    fin = request.args.get('fin')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT tipo, monto, fecha FROM entradas
            WHERE usuario_id = %s AND fecha BETWEEN %s AND %s
        """, (usuario_id, inicio, fin))
        entradas = cursor.fetchall()

        cursor.execute("""
            SELECT tipo, monto, fecha FROM salidas
            WHERE usuario_id = %s AND fecha BETWEEN %s AND %s
        """, (usuario_id, inicio, fin))
        salidas = cursor.fetchall()

    conn.close()
    return jsonify({
        "entradas": entradas,
        "salidas": salidas
    })

@reportes_bp.route('/balance/pdf/<int:usuario_id>', methods=['GET'])
def balance_pdf(usuario_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT SUM(monto) as total_entradas FROM entradas WHERE usuario_id = %s", (usuario_id,))
        total_entradas = cursor.fetchone()['total_entradas'] or 0

        cursor.execute("SELECT SUM(monto) as total_salidas FROM salidas WHERE usuario_id = %s", (usuario_id,))
        total_salidas = cursor.fetchone()['total_salidas'] or 0

    conn.close()
    balance_total = total_entradas - total_salidas

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setTitle("Reporte de Balance")

    # Encabezado
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 750, "Reporte de Balance")

    p.setFont("Helvetica", 12)
    p.drawString(50, 710, f"Usuario ID: {usuario_id}")
    p.drawString(50, 690, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Datos de balance
    p.drawString(50, 640, f"Total de Entradas: ${total_entradas:.2f}")
    p.drawString(50, 620, f"Total de Salidas: ${total_salidas:.2f}")
    p.drawString(50, 600, f"Balance Final: ${balance_total:.2f}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="balance.pdf", mimetype='application/pdf')