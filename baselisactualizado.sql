DROP DATABASE IF EXISTS sistema_financiero;
CREATE DATABASE sistema_financiero CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE sistema_financiero;

-- Tabla de usuarios
CREATE TABLE usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  rol ENUM('admin', 'empleado') DEFAULT 'empleado'
);

-- Tabla de productos
CREATE TABLE productos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  precio DECIMAL(10,2) NOT NULL,
  detalles TEXT,
  cantidad INT DEFAULT 0,
  imagen VARCHAR(255)
);

-- Tabla de entradas
CREATE TABLE entradas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT,
  tipo VARCHAR(100),
  monto DECIMAL(10,2),
  fecha DATE,
  factura_ruta VARCHAR(255),
  imagen_articulo VARCHAR(255),
  cantidad INT DEFAULT 1,
  producto_id INT,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla de salidas
CREATE TABLE salidas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT,
  tipo VARCHAR(100),
  monto DECIMAL(10,2),
  fecha DATE,
  factura_ruta VARCHAR(255),
  cantidad INT DEFAULT 1,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Datos iniciales para usuarios
INSERT INTO usuarios (id, username, password_hash, rol) VALUES
  (1, 'admin', 'admin123', 'admin'),
  (2, 'fer', '1234', 'empleado');
