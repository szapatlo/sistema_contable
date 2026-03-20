CREATE DATABASE sis_contable;

CREATE TABLE usuarios (
id INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(80) UNIQUE NOT NULL,
password_hash VARCHAR(200) NOT NULL,
nombre VARCHAR(200),
role ENUM('admin','contador','auditor') DEFAULT 'contador',
creado_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Tabla cuentas (PUC simplificado)
CREATE TABLE cuentas (
id INT AUTO_INCREMENT PRIMARY KEY,
codigo VARCHAR(30) NOT NULL UNIQUE,
nombre VARCHAR(200) NOT NULL,
tipo ENUM('ACTIVO','PASIVO','PATRIMONIO','INGRESO','GASTO') NOT NULL,
naturaleza ENUM('DEUDORA','ACREDITORA') NOT NULL,
detalle BOOLEAN DEFAULT TRUE,
creado_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Asientos y detalle
CREATE TABLE asientos (
id INT AUTO_INCREMENT PRIMARY KEY,
fecha DATE NOT NULL,
descripcion VARCHAR(255),
creado_por INT,
creado_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (creado_por) REFERENCES usuarios(id) ON DELETE SET NULL
);


CREATE TABLE asiento_detalle (
id INT AUTO_INCREMENT PRIMARY KEY,
asiento_id INT NOT NULL,
cuenta_id INT NOT NULL,
debe DECIMAL(18,2) DEFAULT 0,
haber DECIMAL(18,2) DEFAULT 0,
descripcion VARCHAR(255),
FOREIGN KEY (asiento_id) REFERENCES asientos(id) ON DELETE CASCADE,
FOREIGN KEY (cuenta_id) REFERENCES cuentas(id) ON DELETE RESTRICT
);


-- Datos iniciales (ejemplo PUC simplificado)
INSERT IGNORE INTO cuentas (codigo,nombre,tipo,naturaleza) VALUES
('1105','Caja','ACTIVO','DEUDORA'),
('1305','Clientes','ACTIVO','DEUDORA'),
('2105','Proveedores','PASIVO','ACREDITORA'),
('3105','Capital','PATRIMONIO','ACREDITORA'),
('4105','Ventas','INGRESO','ACREDITORA'),
('5105','Costo de Ventas','GASTO','DEUDORA'),
('6105','Gastos Operativos','GASTO','DEUDORA');

use sis_contable;
select database();
INSERT INTO movimientos (tipo, descripcion, monto)
VALUES ('ingreso','Venta',5000);

INSERT INTO movimientos (tipo, descripcion, monto)
VALUES ('gasto','Compra insumos',2000);
ALTER TABLE usuarios 
ADD COLUMN role VARCHAR(20) DEFAULT 'usuario';
ALTER TABLE usuarios 
ADD COLUMN role VARCHAR(20) DEFAULT 'usuario';

CREATE TABLE empresas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    nit VARCHAR(50) UNIQUE NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(50),
    creado_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);