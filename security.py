from functools import wraps
from flask import session, redirect, url_for, flash

# ===============================
# VERIFICAR USUARIO LOGUEADO
# ===============================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Debe iniciar sesión", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


# ===============================
# VERIFICAR ROL ESPECÍFICO
# ===============================
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "role" not in session:
                flash("Acceso no autorizado", "danger")
                return redirect(url_for("auth.login"))

            if session["role"] not in roles:
                flash("No tiene permisos para acceder", "danger")
                return redirect(url_for("contabilidad.dashboard"))

            return f(*args, **kwargs)
        return decorated_function
    return decorator