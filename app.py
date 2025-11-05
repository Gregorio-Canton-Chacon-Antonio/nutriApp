from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)


USUARIOS_REGISTRADOS = {
    'agregorio.chacon@gmail.com' : {
        'contraseña': 'aGcC.6162008',
        'nombre': 'Antonio',
        'apellidos': 'Gregorio Canton Chacon',
        'fechaDeNacimiento' : '25/01/2008'
    }
}

app.config['SECRET_KEY'] = 'una_clave_secreta_yeaaa'

emails_registrados = ["admin@test.com", "usuario@gmail.com"]

usuarios = {
    'admin@test.com': 'admin123',
    'user@test.com': 'user123',
    'gregorio@cetis61.com': 'mi_password'
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/iniciodesesion", methods=['GET', 'POST'])
def iniciodesesion():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in usuarios and usuarios[email] == password:
            session['logueado'] = True
            session['email'] = email
            flash('¡Inicio de sesión exitoso!')
            return redirect(url_for('index'))
        else:
            flash('Email o contraseña incorrectos')
    
    return render_template('iniciodesesion.html')

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellidos = request.form.get("apellidos")
        email = request.form.get("email")
        contraseña = request.form.get("contraseña")
        confirmaContraseña = request.form.get("confirmAcontraseña")
        
        if email in emails_registrados:
            flash("Este correo electrónico ya está registrado")
            return render_template("registro.html")
        
        if contraseña != confirmaContraseña:
            flash("Las contraseñas no coinciden")
            return render_template("registro.html")
        
        emails_registrados.append(email)
        usuarios[email] = contraseña
        flash(f"Registro exitoso para {nombre} {apellidos}!")
        return redirect(url_for('index'))
    
    return render_template("registro.html")

@app.route("/cuenta")
def cuenta():
    return render_template("cuenta.html")

if __name__ == "__main__":
    app.run(debug=True)