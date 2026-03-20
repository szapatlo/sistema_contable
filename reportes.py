from flask import Blueprint, render_template, send_file
from db import mysql
from security import login_required

import pandas as pd
import io
from reportlab.pdfgen import canvas

reportes_bp = Blueprint("reportes", __name__)

# =========================================
# LIBRO MAYOR
# =========================================
@reportes_bp.route("/libro_mayor")
@login_required
def libro_mayor():

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT 
        c.codigo,
        c.nombre,
        a.fecha,
        d.debe,
        d.haber
    FROM asiento_detalle d
    JOIN cuentas c ON d.cuenta_id = c.id
    JOIN asientos a ON d.asiento_id = a.id
    ORDER BY c.codigo, a.fecha
    """)

    movimientos = cur.fetchall()

    return render_template(
        "libro_mayor.html",
        movimientos=movimientos
    )


# =========================================
# BALANCE GENERAL
# =========================================
@reportes_bp.route("/balance")
@login_required
def balance():

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT
        c.codigo,
        c.nombre,
        c.tipo,
        SUM(d.debe) as total_debe,
        SUM(d.haber) as total_haber
    FROM cuentas c
    LEFT JOIN asiento_detalle d ON c.id = d.cuenta_id
    GROUP BY c.id
    ORDER BY c.codigo
    """)

    cuentas = cur.fetchall()

    activos = []
    pasivos = []
    patrimonio = []

    for c in cuentas:

        saldo = (c[3] or 0) - (c[4] or 0)

        if c[2] == "ACTIVO":
            activos.append((c[0], c[1], saldo))

        elif c[2] == "PASIVO":
            pasivos.append((c[0], c[1], -saldo))

        elif c[2] == "PATRIMONIO":
            patrimonio.append((c[0], c[1], -saldo))

    return render_template(
        "balance.html",
        activos=activos,
        pasivos=pasivos,
        patrimonio=patrimonio
    )


# =========================================
# ESTADO DE RESULTADOS
# =========================================
@reportes_bp.route("/estado_resultados")
@login_required
def estado_resultados():

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT
        c.codigo,
        c.nombre,
        c.tipo,
        SUM(d.debe) as total_debe,
        SUM(d.haber) as total_haber
    FROM cuentas c
    LEFT JOIN asiento_detalle d ON c.id = d.cuenta_id
    WHERE c.tipo IN ('INGRESO','GASTO')
    GROUP BY c.id
    ORDER BY c.codigo
    """)

    cuentas = cur.fetchall()

    ingresos = []
    gastos = []

    for c in cuentas:

        saldo = (c[4] or 0) - (c[3] or 0)

        if c[2] == "INGRESO":
            ingresos.append((c[0], c[1], saldo))

        elif c[2] == "GASTO":
            gastos.append((c[0], c[1], -saldo))

    return render_template(
        "estado_resultados.html",
        ingresos=ingresos,
        gastos=gastos
    )


# =========================================
# EXPORTAR BALANCE A PDF
# =========================================
@reportes_bp.route("/balance_pdf")
@login_required
def balance_pdf():

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer)

    p.drawString(200, 800, "BALANCE GENERAL")
    p.drawString(200, 770, "Sistema Contable")
    p.drawString(200, 740, "Reporte generado automáticamente")

    p.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="balance.pdf",
        mimetype="application/pdf"
    )


# =========================================
# EXPORTAR BALANCE A EXCEL
# =========================================
@reportes_bp.route("/balance_excel")
@login_required
def balance_excel():

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT c.codigo, c.nombre, SUM(d.debe), SUM(d.haber)
    FROM cuentas c
    LEFT JOIN asiento_detalle d ON c.id = d.cuenta_id
    GROUP BY c.id
    """)

    datos = cur.fetchall()

    df = pd.DataFrame(datos, columns=["Codigo", "Cuenta", "Debe", "Haber"])

    archivo = "balance.xlsx"

    df.to_excel(archivo, index=False)

    return send_file(
        archivo,
        as_attachment=True
    )