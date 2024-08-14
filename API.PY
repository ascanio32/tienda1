

from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:19961004Omar.@localhost/tienda'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellidos = db.Column(db.String(80), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cedula = db.Column(db.String(20), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)
    cumpleaños = db.Column(db.Date, nullable=False)

    def set_password(self, password):
        self.contraseña = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contraseña, password)

@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    apellidos = data.get('apellidos')
    direccion = data.get('direccion')
    email = data.get('email')
    cedula = data.get('cedula')
    contraseña = data.get('contraseña')
    confirmar_contraseña = data.get('confirmar_contraseña')
    cumpleaños = data.get('cumpleaños')

    if contraseña != confirmar_contraseña:
        return jsonify({"mensaje": "Las contraseñas no coinciden"}), 400

    # Verificar si el usuario ya existe en la base de datos por email o cedula
    usuario_existente = Cliente.query.filter((Cliente.email == email) | (Cliente.cedula == cedula)).first()
    if usuario_existente:
        return jsonify({"mensaje": "El usuario ya existe"}), 400

    nuevo_cliente = Cliente(
        nombre=nombre,
        apellidos=apellidos,
        direccion=direccion,
        email=email,
        cedula=cedula,
        cumpleaños=cumpleaños
    )
    nuevo_cliente.set_password(contraseña)
    db.session.add(nuevo_cliente)
    db.session.commit()
    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        user = Cliente.query.filter_by(email=email).first()

        if user and user.check_password(contraseña):
            if request.headers.get('User-Agent').startswith('Postman'):
                return jsonify({"mensaje": "¡Inicio de sesión exitoso!"}), 200
            else:
                flash('¡Inicio de sesión exitoso!', 'success')
                return render_template('login.html', mensaje='¡Inicio de sesión exitoso!', redirigir=True)
        else:
            if request.headers.get('User-Agent').startswith('Postman'):
                return jsonify({"mensaje": "Correo electrónico o contraseña inválidos"}), 401
            else:
                flash('Correo electrónico o contraseña inválidos', 'danger')
                return render_template('login.html', mensaje='Correo electrónico o contraseña inválidos', redirigir=False)

    return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)