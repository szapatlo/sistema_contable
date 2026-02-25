from flask import Blueprint, render_template
from security import login_required, role_required

contabilidad_bp = Blueprint("contabilidad", __name__)

@contabilidad_bp.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")


@contabilidad_bp.route("/libro_diario")
@login_required
@role_required("admin", "contador")
def libro_diario():
    return render_template("libro_diario.html")