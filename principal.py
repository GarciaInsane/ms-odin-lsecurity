from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret-key"

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'db5012035825.hosting-data.io'
app.config['MYSQL_USER'] = 'dbu2589286'
app.config['MYSQL_PASSWORD'] = 'jjCIzC!U%&aYpH@t5#'
app.config['MYSQL_DB'] = 'dbs10130836'

# Inicialización de la base de datos MySQL
mysql = MySQL(app)

# Página de inicio que exige autenticación
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener los datos del formulario de inicio de sesión
        usuario = request.form['usuario']
        clave = request.form['clave']

        # Buscar al usuario en la base de datos
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (usuario,))
        usuario_encontrado = cursor.fetchone()

        # Verificar la contraseña del usuario encontrado
        if usuario_encontrado and check_password_hash(usuario_encontrado[2], clave):
            # Iniciar sesión del usuario y redirigir a la página de credenciales
            session['usuario'] = usuario
            return redirect(url_for('credenciales'))
        else:
            # Mostrar un mensaje de error si el inicio de sesión falla
            mensaje_error = "Usuario o clave inválidos"
            return render_template('login.html', mensaje_error=mensaje_error)
    else:
        # Mostrar el formulario de inicio de sesión
        return render_template('login.html')

# Página de credenciales que muestra las credenciales almacenadas en la base de datos
@app.route('/credenciales')
def credenciales():
    # Verificar si el usuario ha iniciado sesión
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Obtener todas las credenciales almacenadas en la base de datos
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM credenciales')
    credenciales = cursor.fetchall()

    # Mostrar la página de credenciales con las credenciales almacenadas en la base de datos
    return render_template('credenciales.html', credenciales=credenciales)

# Página de agregar credenciales que permite al usuario agregar nuevas credenciales a la base de datos
@app.route('/agregar_credenciales', methods=['GET', 'POST'])
def agregar_credenciales():
    # Verificar si el usuario ha iniciado sesión
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Obtener los datos del formulario de agregar credenciales
        usuario = request.form['usuario']
        clave = request.form['clave']
        nombre = request.form['nombre']

        # Insertar las nuevas credenciales en la base de datos
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO credenciales(usuario, clave, nombre) VALUES (%s, %s, %s)', (usuario, generate_password_hash(clave), nombre))
        mysql.connection.commit()

                # Redirigir a la página de credenciales
        return redirect(url_for('credenciales'))
    else:
        # Mostrar el formulario de agregar credenciales
        return render_template('agregar_credenciales.html')

# Página de eliminar credenciales que permite al usuario eliminar credenciales de la base de datos
@app.route('/eliminar_credenciales/<string:id>', methods=['POST'])
def eliminar_credenciales(id):
    # Verificar si el usuario ha iniciado sesión
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Eliminar las credenciales de la base de datos
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM credenciales WHERE id = %s', (id,))
    mysql.connection.commit()

    # Redirigir a la página de credenciales
    return redirect(url_for('credenciales'))

# Página de administración que muestra todas las credenciales y permite al administrador controlar los usuarios
@app.route('/administracion')
def administracion():
    # Verificar si el usuario ha iniciado sesión
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Verificar si el usuario es un administrador
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (session['usuario'],))
    usuario_encontrado = cursor.fetchone()

    if not usuario_encontrado or not usuario_encontrado[3]:
        # Mostrar un mensaje de error si el usuario no es un administrador
        mensaje_error = "No tienes permiso para acceder a esta página"
        return render_template('login.html', mensaje_error=mensaje_error)

    # Obtener todas las credenciales almacenadas en la base de datos
    cursor.execute('SELECT * FROM credenciales')
    credenciales = cursor.fetchall()

    # Obtener todos los usuarios almacenados en la base de datos
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()

    # Mostrar la página de administración con todas las credenciales y usuarios almacenados en la base de datos
    return render_template('administracion.html', credenciales=credenciales, usuarios=usuarios)

# Página de agregar usuario que permite al administrador agregar nuevos usuarios a la base de datos
@app.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    # Verificar si el usuario ha iniciado sesión
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Verificar si el usuario es un administrador
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (session['usuario'],))
    usuario_encontrado = cursor.fetchone()

    if not usuario_encontrado or not usuario_encontrado[3]:
        # Mostrar un mensaje de error si el usuario no es un administrador
        mensaje_error = "No tienes permiso para acceder a esta página"
        return render_template('login.html', mensaje_error=mensaje_error)

    if request.method == 'POST':
        # Obtener los datos del formulario de agregar usuario
        usuario = request.form['usuario']
        clave = request.form['clave']
        es_administrador = request.form.get('es_administrador') is not None

        # Insertar el nuevo usuario en la base de datos
        cursor = mysql.connection.cursor

        cursor.execute('INSERT INTO usuarios(usuario, clave, es_administrador) VALUES (%s, %s, %s)', (usuario, clave, es_administrador))
        mysql.connection.commit()

        # Redirigir a la página de administración
        return redirect(url_for('administracion'))
    else:
        # Mostrar el formulario de agregar usuario
        return render_template('agregar_usuario.html')

# Página de eliminar usuario que permite al administrador eliminar usuarios de la base de datos
@app.route('/eliminar_usuario/<string:id>', methods=['POST'])
def eliminar_usuario(id):
    # Verificar si el usuario ha iniciado sesión
    if 'usuario' not in session:
        return redirect(url_for('login'))

    # Verificar si el usuario es un administrador
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (session['usuario'],))
    usuario_encontrado = cursor.fetchone()

    if not usuario_encontrado or not usuario_encontrado[3]:
        # Mostrar un mensaje de error si el usuario no es un administrador
        mensaje_error = "No tienes permiso para acceder a esta página"
        return render_template('login.html', mensaje_error=mensaje_error)

    # Eliminar el usuario de la base de datos
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
    mysql.connection.commit()

    # Redirigir a la página de administración
    return redirect(url_for('administracion'))
