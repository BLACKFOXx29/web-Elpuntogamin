from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, IntegerField, FileField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(3, 80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(6, 128)])
    password2 = PasswordField('Repite la contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Iniciar sesión')

class EventoForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    fecha = DateTimeField('Fecha (YYYY-MM-DD HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Guardar evento')

class ImagenForm(FlaskForm):
    file = FileField('Seleccionar imagen', validators=[DataRequired()])
    descripcion = StringField('Descripción')
    submit = SubmitField('Subir imagen')

class MensajeForm(FlaskForm):
    autor = StringField('Nombre', validators=[DataRequired()])
    contenido = TextAreaField('Mensaje', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Enviar')

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción')
    precio = FloatField('Precio', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    submit = SubmitField('Guardar producto')

class EditProfileForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Biografía', validators=[Length(max=500)])
    avatar = FileField('Avatar')
    submit = SubmitField('Guardar Cambios')
