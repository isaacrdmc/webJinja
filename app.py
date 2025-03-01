from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from markupsafe import escape


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length







app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'  # ? Definimos la clave secreta

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


# ? Definimos la clase para poder crear la Base De Datos
class Usuario(db.Model):
    id = db.Column(db.Integer, pimary_key=True)
    usuario = db.Column(db.String(15), unique=True, nullable=False)
    contrasena = db.Column(db.String(8), nullable=False)





# ? Definimos la clase para utilizar los omoponentes
class MiFormularioLogin(FlaskForm):
    usuario = StringField('Username', validators=[InputRequired('Usuario requerido'), Length(min=5, max=25, message='El usuario no con los requisitos')])
    contraseña = PasswordField('Passowrd', validators=[InputRequired('Contraseña requerida')])
    enviarmos = SubmitField('Enviar')
    registro = SubmitField('Registro')


# ? Definimos la ruta para el formulario,
# ? Para esto vamos a recibir los datos del formualrio
@app.route('/form', methods=['GET', 'POST'])
def form ():
    form = MiFormularioLogin()
    if form.validate_on_submit():
        return '<h1> Hola {}!!. Tú formulario se ha enviado correctamente!! </h1>'.format(form.usuario.data)
    return render_template('login.html', form=form)



# * Ejecutamos la aplicación
if __name__ == '__main__': 
	app.run(debug=True)
