from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'  # Clave secreta
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

# Modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(15), unique=True, nullable=False)
    contrasena = db.Column(db.String(128), nullable=False)

# Creación de la BD
with app.app_context():
    db.create_all()

# Formulario
class MiFormularioLogin(FlaskForm):
    usuario = StringField(
        'Ingresa el usuario', 
        validators=[InputRequired('Usuario requerido'), Length(min=5, max=25)]
    )
    contraseña = PasswordField(
        'Ingresa la contraseña', 
        validators=[InputRequired('Contraseña requerida')]
    )
    enviarmos = SubmitField('Iniciar sesión')
    registro = SubmitField('Registro')

# Ruta para el formulario de login
@app.route('/form', methods=['GET', 'POST'])
def form():
    form = MiFormularioLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(usuario=form.usuario.data).first()
        if usuario and check_password_hash(usuario.contrasena, form.contraseña.data):
            return redirect(url_for('bienvenido', usuario=form.usuario.data))
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
            return redirect(url_for('form'))

    return render_template('login.html', form=form)

# Ruta para la pantalla de bienvenida
@app.route('/bienvenido/<usuario>')
def bienvenido(usuario):
    return render_template('bienvenido.html', usuario=usuario)

# Ruta de registro
@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    form = MiFormularioLogin()
    if form.validate_on_submit():
        usuario_existente = Usuario.query.filter_by(usuario=form.usuario.data).first()
        if usuario_existente:
            flash(f'El usuario {form.usuario.data} ya está registrado.', 'error')
            return redirect(url_for('registro'))

        nuevo_usuario = Usuario(
            usuario=form.usuario.data, 
            contrasena=generate_password_hash(form.contraseña.data)
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario registrado correctamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('form'))

    return render_template('registro.html', form=form)

if __name__ == '__main__': 
    app.run(debug=True)
