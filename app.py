import os
from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
from config import Config
from models import db, User, Miembro, Evento, Imagen, Mensaje, Producto
from forms import RegisterForm, LoginForm, EventoForm, ImagenForm, MensajeForm, ProductoForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
from forms import EditProfileForm


# --------------------------
# FUNCIONES AUXILIARES
# --------------------------

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


# --------------------------
# CONFIGURACIÓN PRINCIPAL
# --------------------------

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Crear carpeta uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_datetime():
    return {'datetime': datetime}


# --------------------------
# RUTAS PÚBLICAS
# --------------------------

@app.route('/')
def index():
    eventos = Evento.query.order_by(Evento.fecha.asc()).limit(3).all()
    imagenes = Imagen.query.order_by(Imagen.uploaded_at.desc()).limit(5).all()
    productos = Producto.query.limit(3).all()
    return render_template('index.html', eventos=eventos, imagenes=imagenes, productos=productos)


# --------------------------
# REGISTRO
# --------------------------

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # evitar usuarios repetidos
        if User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first():
            flash('Usuario o email ya registrado', 'warning')
            return redirect(url_for('register'))

        hashed = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed)
        db.session.add(user)
        db.session.commit()

        # Añadir a tabla Miembro
        miembro = Miembro(nombre=form.username.data, usuario=form.username.data, bio='Nuevo miembro')
        db.session.add(miembro)
        db.session.commit()

        flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# --------------------------
# LOGIN / LOGOUT
# --------------------------

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Has iniciado sesión', 'success')
            return redirect(url_for('index'))
        flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('index'))


# --------------------------
# PERFIL DEL USUARIO
# --------------------------

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

# --------------------------
# EDITAR PERFIL
# --------------------------

@app.route('/editar_perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = EditProfileForm()

    if form.validate_on_submit():

        # Actualizar nombre, email y bio
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data

        # Procesar avatar nuevo
        if form.avatar.data:
            file = form.avatar.data
            filename = secure_filename(f"avatar_{current_user.id}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            current_user.avatar = filename

        db.session.commit()
        flash("Perfil actualizado con éxito", "success")
        return redirect(url_for('perfil'))

    # Cargar valores actuales
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.bio.data = current_user.bio

    return render_template('editar_perfil.html', form=form)


# --------------------------
# MIEMBROS, EVENTOS, GALERÍA
# --------------------------

@app.route('/miembros')
def miembros():
    lista = Miembro.query.order_by(Miembro.joined.desc()).all()
    return render_template('miembros.html', miembros=lista)


@app.route('/eventos')
def eventos():
    lista = Evento.query.order_by(Evento.fecha.asc()).all()
    return render_template('eventos.html', eventos=lista)


@app.route('/galeria')
def galeria():
    imgs = Imagen.query.order_by(Imagen.uploaded_at.desc()).all()
    return render_template('galeria.html', imagenes=imgs)


@app.route('/subir_galeria', methods=['GET','POST'])
@login_required
def subir_galeria():
    form = ImagenForm()
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{datetime.utcnow().timestamp()}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            imagen = Imagen(filename=filename, descripcion=form.descripcion.data)
            db.session.add(imagen)
            db.session.commit()

            flash('Imagen subida con éxito', 'success')
            return redirect(url_for('galeria'))

        flash('Formato no permitido', 'danger')

    return render_template('subir_galeria.html', form=form)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# --------------------------
# FORO
# --------------------------

@app.route('/foro', methods=['GET','POST'])
def foro():
    form = MensajeForm()
    if form.validate_on_submit():
        msg = Mensaje(autor=form.autor.data, contenido=form.contenido.data)
        db.session.add(msg)
        db.session.commit()

        flash('Mensaje publicado', 'success')
        return redirect(url_for('foro'))

    mensajes = Mensaje.query.order_by(Mensaje.created_at.desc()).all()
    return render_template('foro.html', form=form, mensajes=mensajes)


# --------------------------
# TIENDA Y PRODUCTOS
# --------------------------

@app.route('/tienda')
def tienda():
    productos = Producto.query.all()
    return render_template('tienda.html', productos=productos)


@app.route('/producto/<int:product_id>')
def producto(product_id):
    p = Producto.query.get_or_404(product_id)
    return render_template('producto.html', producto=p)


# --------------------------
# ADMINISTRACIÓN
# --------------------------

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acceso requerido: administrador', 'danger')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper


@app.route('/admin', methods=['GET','POST'])
@admin_required
def admin():
    eform = EventoForm(prefix='e')
    pform = ProductoForm(prefix='p')

    if eform.validate_on_submit() and eform.submit.data:
        evt = Evento(
            titulo=eform.titulo.data,
            descripcion=eform.descripcion.data,
            fecha=eform.fecha.data
        )
        db.session.add(evt)
        db.session.commit()

        flash('Evento creado', 'success')
        return redirect(url_for('admin'))

    if pform.validate_on_submit() and pform.submit.data:
        prod = Producto(
            nombre=pform.nombre.data,
            descripcion=pform.descripcion.data,
            precio=pform.precio.data,
            stock=pform.stock.data
        )
        db.session.add(prod)
        db.session.commit()

        flash('Producto creado', 'success')
        return redirect(url_for('admin'))

    eventos = Evento.query.order_by(Evento.fecha.asc()).all()
    productos = Producto.query.all()

    return render_template('admin.html', eform=eform, pform=pform, eventos=eventos, productos=productos)



# --------------------------
# EJECUCIÓN LOCAL
# --------------------------

if __name__ == '__main__':
    app.run(debug=True)
