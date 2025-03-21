from flask import Flask, render_template
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
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
