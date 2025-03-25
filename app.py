from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import os

from controllers.auth_controller import auth_bp
from controllers.entradas_controller import entradas_bp
from controllers.salidas_controller import salidas_bp
from controllers.reportes_controller import reportes_bp
from controllers.productos_controller import productos_bp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
CORS(app)

# Crear carpeta de imágenes si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(entradas_bp, url_prefix='/api/entradas')
app.register_blueprint(salidas_bp, url_prefix='/api/salidas')
app.register_blueprint(reportes_bp, url_prefix='/api/reportes')
app.register_blueprint(productos_bp)

# Ruta raíz para documentación básica
@app.route('/')
def home():
    return render_template('documentacion.html')  # Esto apunta a templates/index.html

@app.route('/inicio')
def inicio():
    return render_template('index.html')  # Esto busca en la carpeta "templates"

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Esto apunta a templates/dashboard.html

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
