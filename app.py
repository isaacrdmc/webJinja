from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash

# ? Configuraión de la BD y flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'  # Creamos la clave secreta
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'  # Definimos el archivo de la BD que se llamara 'db.sqlite'
db = SQLAlchemy(app)


# ? Modelo de usuario
# Le decimos que se valla a la tabla del usuario que sera donde almacenara lo siguiente:
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(15), unique=True, nullable=False)
    contrasena = db.Column(db.String(128), nullable=False)

# ? Creamos la tabla 'Usuario' si es que aun no existe
with app.app_context():
    db.create_all()



# ? Creamos la sección del Formulario
class MiFormularioLogin(FlaskForm):
    usuario = StringField(      # Campo de entrada
        'Ingresa el usuario', 
        validators=[InputRequired('Usuario requerido'), Length(min=5, max=25)]      # Hacemos al comapo obligatorio para que no se lo salte
    )
    contraseña = PasswordField(      # Campo de entrada
        'Ingresa la contraseña', 
        validators=[InputRequired('Contraseña requerida')]      # Hacemos al comapo obligatorio para que no se lo salte
    )

    # * Botones de funcion dentro del ormulario
    enviarmos = SubmitField('Iniciar sesión')
    registro = SubmitField('Registro')




# ? Deinimos la ruta para el formulario de login
@app.route('/form', methods=['GET', 'POST'])
def form():
    # Mandamos a llamar la clase del formulario
    form = MiFormularioLogin()

    # Si se ha enviado se analizara todo lo siguiente
    if form.validate_on_submit():
        # Filtramos para buscar al usuarios dentro de la BD
        usuario = Usuario.query.filter_by(usuario=form.usuario.data).first()

        # Ahora vefiricamos que la contraseña exista y si existe le damos la bienvenida
        if usuario and check_password_hash(usuario.contrasena, form.contraseña.data):
            return redirect(url_for('bienvenido', usuario=form.usuario.data))
        
            # En caso contrario le informamos de eso
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
            return redirect(url_for('form'))

    return render_template('login.html', form=form)



# ? Ruta para la pantalla de bienvenida
@app.route('/bienvenido/<usuario>')
def bienvenido(usuario):
    return render_template('bienvenido.html', usuario=usuario)



# ? Ruta para el registro del usuario
@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    form = MiFormularioLogin()

    # Cuando el formualrio se envie primero validamos si ya existe este usuario en la BD
    if form.validate_on_submit():
        usuario_existente = Usuario.query.filter_by(usuario=form.usuario.data).first()
        if usuario_existente:
            flash(f'El usuario {form.usuario.data} ya está registrado.', 'error')
            return redirect(url_for('registro'))

        # Si no existe lo alamcenamos dentro de la BD
        nuevo_usuario = Usuario(
            usuario=form.usuario.data, 
            contrasena=generate_password_hash(form.contraseña.data) # * Ciframos la contraseña con un hash por seguridad
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario registrado correctamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('form'))

    return render_template('registro.html', form=form)


# ? Ejecutamos el sitio
if __name__ == '__main__': 
    app.run(debug=True)
