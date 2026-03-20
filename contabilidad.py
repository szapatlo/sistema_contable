from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import mysql
from security import login_required, role_required

contabilidad_bp = Blueprint("contabilidad", __name__)

# ======================================
# DASHBOARD CONTABLE
# ======================================
@contabilidad_bp.route("/")
@login_required
def dashboard():

    cur = mysql.connection.cursor()

    # ACTIVOS
    cur.execute("""
    SELECT SUM(d.debe - d.haber)
    FROM asiento_detalle d
    JOIN cuentas c ON d.cuenta_id = c.id
    WHERE c.tipo='ACTIVO'
    """)
    activos = cur.fetchone()[0] or 0

    # PASIVOS
    cur.execute("""
    SELECT SUM(d.haber - d.debe)
    FROM asiento_detalle d
    JOIN cuentas c ON d.cuenta_id = c.id
    WHERE c.tipo='PASIVO'
    """)
    pasivos = cur.fetchone()[0] or 0

    # PATRIMONIO
    cur.execute("""
    SELECT SUM(d.haber - d.debe)
    FROM asiento_detalle d
    JOIN cuentas c ON d.cuenta_id = c.id
    WHERE c.tipo='PATRIMONIO'
    """)
    patrimonio = cur.fetchone()[0] or 0

    # INGRESOS
    cur.execute("""
    SELECT SUM(d.haber - d.debe)
    FROM asiento_detalle d
    JOIN cuentas c ON d.cuenta_id = c.id
    WHERE c.tipo='INGRESO'
    """)
    ingresos = cur.fetchone()[0] or 0

    # GASTOS
    cur.execute("""
    SELECT SUM(d.debe - d.haber)
    FROM asiento_detalle d
    JOIN cuentas c ON d.cuenta_id = c.id
    WHERE c.tipo='GASTO'
    """)
    gastos = cur.fetchone()[0] or 0

    utilidad = ingresos - gastos

    return render_template(
        "dashboard.html",
        activos=activos,
        pasivos=pasivos,
        patrimonio=patrimonio,
        utilidad=utilidad
    )


# ======================================
# LIBRO DIARIO
# ======================================
@contabilidad_bp.route("/libro_diario", methods=["GET", "POST"])
@login_required
@role_required("admin", "contador")
def libro_diario():

    cur = mysql.connection.cursor()

    # Obtener cuentas contables
    cur.execute("SELECT id, codigo, nombre FROM cuentas ORDER BY codigo")
    cuentas = cur.fetchall()

    if request.method == "POST":

        fecha = request.form["fecha"]
        descripcion = request.form["descripcion"]

        cuenta_ids = request.form.getlist("cuenta_id")
        debe = request.form.getlist("debe")
        haber = request.form.getlist("haber")

        total_debe = sum(float(d or 0) for d in debe)
        total_haber = sum(float(h or 0) for h in haber)

        if total_debe != total_haber:
            flash("El asiento no está balanceado (Debe ≠ Haber)", "danger")
            return redirect(url_for("contabilidad.libro_diario"))

        # Guardar asiento
        cur.execute("""
        INSERT INTO asientos (fecha, descripcion, creado_por)
        VALUES (%s,%s,%s)
        """, (fecha, descripcion, session["user_id"]))

        asiento_id = cur.lastrowid

        # Guardar detalle
        for i in range(len(cuenta_ids)):

            valor_debe = float(debe[i] or 0)
            valor_haber = float(haber[i] or 0)

            if valor_debe > 0 or valor_haber > 0:

                cur.execute("""
                INSERT INTO asiento_detalle
                (asiento_id, cuenta_id, debe, haber)
                VALUES (%s,%s,%s,%s)
                """, (
                    asiento_id,
                    cuenta_ids[i],
                    valor_debe,
                    valor_haber
                ))

        mysql.connection.commit()

        flash("Asiento guardado correctamente", "success")

        return redirect(url_for("contabilidad.libro_diario"))

    # ===============================
    # MOSTRAR MOVIMIENTOS
    # ===============================
    cur.execute("""
    SELECT a.fecha, a.descripcion, c.codigo, c.nombre, d.debe, d.haber
    FROM asientos a
    JOIN asiento_detalle d ON a.id = d.asiento_id
    JOIN cuentas c ON d.cuenta_id = c.id
    ORDER BY a.fecha DESC
    """)

    movimientos = cur.fetchall()

    return render_template(
        "libro_diario.html",
        cuentas=cuentas,
        movimientos=movimientos
    )