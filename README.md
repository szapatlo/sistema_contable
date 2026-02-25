# Sistema Contable Web – Proyecto Final

Sistema contable web desarrollado en Python con Flask y MySQL, orientado a la gestión contable bajo principios básicos del PUC colombiano.

## Tecnologías utilizadas

- Python 3
- Flask
- MySQL
- Flask-MySQLdb
- Bootstrap 5
- Jinja2
- Git y GitHub

## Funcionalidades implementadas

- Autenticación de usuarios con roles (admin, contador, auditor)
- Control de acceso por módulo (RBAC)
- Gestión de empresas
- Libro diario
- Balance general
- Estado de resultados
- Validación contable básica
- Seguridad mediante contraseñas encriptadas
- Arquitectura modular con Blueprints

## Arquitectura

El sistema está desarrollado bajo un enfoque modular utilizando Blueprints de Flask para separar:

- Autenticación
- Seguridad
- Contabilidad
- Reportes
- Gestión de empresas

## Base de datos

Base de datos relacional MySQL con:

- Usuarios
- Empresas
- Cuentas contables (PUC simplificado)
- Asientos contables
- Detalle de asientos

## Seguridad implementada

- Hash seguro de contraseñas
- Consultas parametrizadas
- Protección de rutas
- Control de sesión
- Separación de roles

## Cómo ejecutar el proyecto

1. Clonar el repositorio
2. Crear entorno virtual
3. Instalar dependencias:
   pip install -r requirements.txt
4. Configurar base de datos en config.py
5. Ejecutar:
   python app.py

## Autor

Sebastián Zapata
Proyecto académico – 2026
