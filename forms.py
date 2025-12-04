from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Optional

class RegisterForm(FlaskForm):
    username = StringField(
        "Usuario",
        validators=[DataRequired(message="El usuario es obligatorio"), Length(min=3, max=30)]
    )
    email = StringField(
        "Email",
        validators=[Optional(), Email(message="Introduce un email válido")]
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(message="La contraseña es obligatoria"), Length(min=6)]
    )
    password2 = PasswordField(
        "Repite la contraseña",
        validators=[DataRequired(message="Repite la contraseña"), EqualTo('password', message="Las contraseñas no coinciden")]
    )
    submit = SubmitField("Registrarse")

class LoginForm(FlaskForm):
    username = StringField(
        "Usuario",
        validators=[DataRequired(message="El usuario es obligatorio")]
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(message="La contraseña es obligatoria")]
    )
    remember = BooleanField("Recordarme")
    submit = SubmitField("Iniciar sesión")

class ForoPostForm(FlaskForm):
    contenido = TextAreaField(
        "Mensaje",
        validators=[DataRequired(message="Escribe algo"), Length(min=1, max=2000, message="Máximo 2000 caracteres")]
    )
    submit = SubmitField("Publicar")

