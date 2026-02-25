from flask import Blueprint, render_template
from db import mysql
from security import login_required, role_required

reportes_bp = Blueprint("reportes", __name__)

# ======================================================
# BALANCE GENERAL
# ======================================================
@reportes_bp.route("/balance")
@login_required
@role_required("admin", "contador", "auditor")
def balance():

    cur = mysql.connection.cursor()

    # ACTIVO
    cur.execute("""
        SELECT c.codigo, c.nombre,
        COALESCE(SUM(ad.debe - ad.haber), 0) AS saldo
        FROM cuentas c
        LEFT JOIN asiento_detalle ad ON ad.cuenta_id = c.id
        WHERE c.tipo = 'ACTIVO'
        GROUP BY c.id
    """)
    activos = cur.fetchall()

    # PASIVO
    cur.execute("""
        SELECT c.codigo, c.nombre,
        COALESCE(SUM(ad.haber - ad.debe), 0) AS saldo
        FROM cuentas c
        LEFT JOIN asiento_detalle ad ON ad.cuenta_id = c.id
        WHERE c.tipo = 'PASIVO'
        GROUP BY c.id
    """)
    pasivos = cur.fetchall()

    # PATRIMONIO
    cur.execute("""
        SELECT c.codigo, c.nombre,
        COALESCE(SUM(ad.haber - ad.debe), 0) AS saldo
        FROM cuentas c
        LEFT JOIN asiento_detalle ad ON ad.cuenta_id = c.id
        WHERE c.tipo = 'PATRIMONIO'
        GROUP BY c.id
    """)
    patrimonio = cur.fetchall()

    return render_template(
        "balance.html",
        activos=activos,
        pasivos=pasivos,
        patrimonio=patrimonio
    )


# ======================================================
# ESTADO DE RESULTADOS
# ======================================================
@reportes_bp.route("/estado_resultados")
@login_required
@role_required("admin", "contador", "auditor")
def estado_resultados():

    cur = mysql.connection.cursor()

    # INGRESOS
    cur.execute("""
        SELECT c.codigo, c.nombre,
        COALESCE(SUM(ad.haber - ad.debe), 0) AS saldo
        FROM cuentas c
        LEFT JOIN asiento_detalle ad ON ad.cuenta_id = c.id
        WHERE c.tipo = 'INGRESO'
        GROUP BY c.id
    """)
    ingresos = cur.fetchall()

    # GASTOS
    cur.execute("""
        SELECT c.codigo, c.nombre,
        COALESCE(SUM(ad.debe - ad.haber), 0) AS saldo
        FROM cuentas c
        LEFT JOIN asiento_detalle ad ON ad.cuenta_id = c.id
        WHERE c.tipo = 'GASTO'
        GROUP BY c.id
    """)
    gastos = cur.fetchall()

    return render_template(
        "estado_resultados.html",
        ingresos=ingresos,
        gastos=gastos
    )