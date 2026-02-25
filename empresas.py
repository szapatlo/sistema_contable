from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import mysql
from security import login_required, role_required

empresas_bp = Blueprint("empresas", __name__)

# ======================================================
# LISTAR Y CREAR EMPRESAS
# ======================================================
@empresas_bp.route("/empresas", methods=["GET", "POST"])
@login_required
@role_required("admin")
def listar_empresas():

    cur = mysql.connection.cursor()

    if request.method == "POST":
        nombre = request.form.get("nombre")
        nit = request.form.get("nit")
        direccion = request.form.get("direccion")
        telefono = request.form.get("telefono")

        if not nombre or not nit:
            flash("Nombre y NIT son obligatorios", "danger")
            return redirect(url_for("empresas.listar_empresas"))

        # Verificar NIT duplicado
        cur.execute("SELECT id FROM empresas WHERE nit=%s", (nit,))
        existente = cur.fetchone()

        if existente:
            flash("Ya existe una empresa con ese NIT", "warning")
            return redirect(url_for("empresas.listar_empresas"))

        cur.execute("""
            INSERT INTO empresas (nombre, nit, direccion, telefono)
            VALUES (%s, %s, %s, %s)
        """, (nombre, nit, direccion, telefono))

        mysql.connection.commit()
        flash("Empresa creada correctamente", "success")
        return redirect(url_for("empresas.listar_empresas"))

    cur.execute("SELECT * FROM empresas ORDER BY id DESC")
    empresas = cur.fetchall()
    cur.close()

    return render_template("empresas.html", empresas=empresas)


# ======================================================
# EDITAR EMPRESA
# ======================================================
@empresas_bp.route("/empresas/editar/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def editar_empresa(id):

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM empresas WHERE id=%s", (id,))
    empresa = cur.fetchone()

    if not empresa:
        flash("Empresa no encontrada", "danger")
        return redirect(url_for("empresas.listar_empresas"))

    if request.method == "POST":
        nombre = request.form.get("nombre")
        nit = request.form.get("nit")
        direccion = request.form.get("direccion")
        telefono = request.form.get("telefono")

        cur.execute("""
            UPDATE empresas
            SET nombre=%s, nit=%s, direccion=%s, telefono=%s
            WHERE id=%s
        """, (nombre, nit, direccion, telefono, id))

        mysql.connection.commit()
        flash("Empresa actualizada correctamente", "success")
        return redirect(url_for("empresas.listar_empresas"))

    cur.close()
    return render_template("editar_empresa.html", empresa=empresa)


# ======================================================
# ELIMINAR EMPRESA
# ======================================================
@empresas_bp.route("/empresas/eliminar/<int:id>")
@login_required
@role_required("admin")
def eliminar_empresa(id):

    cur = mysql.connection.cursor()

    cur.execute("SELECT id FROM empresas WHERE id=%s", (id,))
    empresa = cur.fetchone()

    if not empresa:
        flash("Empresa no encontrada", "danger")
        return redirect(url_for("empresas.listar_empresas"))

    cur.execute("DELETE FROM empresas WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    flash("Empresa eliminada correctamente", "warning")
    return redirect(url_for("empresas.listar_empresas"))