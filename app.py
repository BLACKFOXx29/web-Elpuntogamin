from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# -----------------------------
# Models
# -----------------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

class ForoPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.String(100))
    contenido = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

# -----------------------------
# Login Manager
# -----------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -----------------------------
# Context: Fecha global
# -----------------------------

@app.context_processor
def inject_datetime():
    return {"datetime": datetime}

# -----------------------------
# Rutas del sitio
# -----------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/miembros")
def miembros():
    return render_template("miembros.html")

@app.route("/eventos")
def eventos():
    return render_template("eventos.html")

@app.route("/tienda")
def tienda():
    return render_template("tienda.html")

@app.route("/foro", methods=["GET", "POST"])
def foro():
    if request.method == "POST":
        if not current_user.is_authenticated:
            flash("Debes iniciar sesión para publicar.")
            return redirect(url_for("login"))

        contenido = request.form.get("contenido")
        post = ForoPost(autor=current_user.username, contenido=contenido)
        db.session.add(post)
        db.session.commit()

    posts = ForoPost.query.order_by(ForoPost.fecha.desc()).all()
    return render_template("foro.html", posts=posts)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            flash("El usuario ya existe.")
            return redirect(url_for("register"))

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Registro completado, ahora inicia sesión.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for("index"))
        flash("Credenciales incorrectas.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
