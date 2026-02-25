from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import mysql

auth_bp = Blueprint("auth", __name__)  # IMPORTANTE: sin url_prefix


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, password_hash, role FROM usuarios WHERE username=%s", (username,))
        user = cur.fetchone()

        if not user:
            flash("El usuario no existe", "danger")
            return render_template("login.html")

        if not check_password_hash(user[2], password):
            flash("Contraseña incorrecta", "danger")
            return render_template("login.html")

        session["user_id"] = user[0]
        session["username"] = user[1]
        session["role"] = user[3]

        return redirect(url_for("contabilidad.dashboard"))

    return render_template("login.html")


# =========================
# REGISTER (SOLO ADMIN)
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    # Solo admin puede acceder
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "admin":
        return "Acceso denegado", 403

    if request.method == "POST":
        nombre = request.form.get("nombre")
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM usuarios WHERE username=%s", (username,))
        existente = cur.fetchone()

        if existente:
            flash("El usuario ya existe", "warning")
            return render_template("register.html")

        cur.execute("""
            INSERT INTO usuarios (username, password_hash, nombre, role)
            VALUES (%s, %s, %s, %s)
        """, (username, hashed_password, nombre, role))

        mysql.connection.commit()

        flash("Usuario creado correctamente", "success")
        return redirect(url_for("contabilidad.dashboard"))

    return render_template("register.html")


# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))