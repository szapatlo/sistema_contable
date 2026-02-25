from flask import Flask
from config import Config
from db import mysql

from auth import auth_bp
from contabilidad import contabilidad_bp
from empresas import empresas_bp
from reportes import reportes_bp

app = Flask(__name__)
app.config.from_object(Config)

mysql.init_app(app)

# REGISTRAR BLUEPRINTS
app.register_blueprint(auth_bp)
app.register_blueprint(contabilidad_bp)
app.register_blueprint(empresas_bp)
app.register_blueprint(reportes_bp)


if __name__ == "__main__":
    app.run(debug=True)