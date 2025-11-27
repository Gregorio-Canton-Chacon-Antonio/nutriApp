from flask import Flask, render_template, request, redirect, url_for, flash, session

from werkzeug.security import generate_password_hash, check_password_hash
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_super_secreta_123'
API_KEY = "fkWcgGrSo0tzA5nBXI0AFFxKuXXdXAzMmtZ0Fz2I"
USDA_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"


@app.route('/buscar', methods=['POST'])
def buscar_alimento():
    alimento = request.form['alimento']
    
    params = {
        'api_key': API_KEY,
        'query': alimento,
        'pageSize': 10  
    }
    
    try:
        response = requests.get(USDA_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        alimentos = data.get('foods', [])
        return render_template('alimento.html', alimentos=alimentos, busqueda=alimento)
            
    except Exception as e:
        flash(f'Error al buscar alimento: {str(e)}')
        return render_template('alimento.html', alimentos=[], busqueda=alimento)


emails = ["admin@test.com", "usuario@gmail.com"]

users = {
    'agregorio.chacon@gmail.com': {
        'password': 'aGcC.6162008',
        'name': 'Antonio',
        'lastname': 'Gregorio Canton Chacon',
        'birthdate': '25/01/2008'
    }
}

current_user = None





@app.route("/")
def index():
    global current_user
    usuario = users.get(current_user) if current_user else None
    return render_template("index.html", usuario=usuario)

@app.route("/sesion", methods=['GET', 'POST'])
def sesion():
    if request.method == 'POST':
        email = request.form['correo']
        password = request.form['contraseña']
        
        if email in users and users[email]['password'] == password:
            global current_user
            current_user = email
            return redirect(url_for('cuenta'))
        else:
            flash('Credenciales incorrectas')
    
    return render_template('sesion.html')


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        name = request.form.get("nombre")
        lastname = request.form.get("apellidos")
        day = request.form.get("dia")
        month = request.form.get("mes")
        year = request.form.get("año")
        gender = request.form.get("genero")
        email = request.form.get("correo")
        password = request.form.get("contraseña")
        confirm_password = request.form.get("confirmaContraseña")
        
        biological_sex = request.form.get("sexo")
        weight = request.form.get("peso")
        height = request.form.get("altura")
        activity_level = request.form.get("nivel de act")
        goal = request.form.get("objetivo")
        cooking_exp = request.form.get("nivel de exp")
        allergies = request.form.get("alergia")
        intolerances = request.form.get("intolerancia")
        disliked_foods = request.form.get("alimentos no gustan")
        
        if email in emails:
            flash("Ya existe una cuenta con este email")
            return render_template("registro.html")
        
        if password != confirm_password:
            flash("Las contraseñas no son iguales")
            return render_template("registro.html")
        
        emails.append(email)
        users[email] = {
            'name': name,
            'lastname': lastname,
            'birthdate': f"{day}/{month}/{year}",
            'gender': gender,
            'email': email,
            'password': password,
            'biological_sex': biological_sex,
            'weight': weight,
            'height': height,
            'activity_level': activity_level,
            'goal': goal,
            'cooking_exp': cooking_exp,
            'allergies': allergies,
            'intolerances': intolerances,
            'disliked_foods': disliked_foods
        }
        
        global current_user
        current_user = email
        return redirect(url_for('cuenta'))
    
    return render_template("registro.html")

@app.route("/cuenta")
def cuenta():
    global current_user
    user_data = None
    user_name = None
    
    if current_user and current_user in users:
        user_data = users[current_user]
        user_name = user_data['name']
    
    return render_template("cuenta.html", usuario=user_data, nombre_usuario=user_name)

@app.route("/cerrar_sesion")
def cerrar_sesion():
    global current_user
    current_user = None
    flash('Has cerrado sesión')
    return redirect(url_for('index'))

@app.route("/dietas")
def dietas():
    return render_template("dietas.html")

@app.route("/calculadoras")
def calculadoras():
    return render_template("calculadoras.html")

@app.route("/calculadora_imc", methods=['GET', 'POST'])
def calculadora_imc():
    return render_template("calculadora_imc.html")

@app.route("/calculadora_tmb", methods=['GET', 'POST'])
def calculadora_tmb():
    return render_template("calculadora_tmb.html")

@app.route("/calculadora_gct", methods=['GET', 'POST'])
def calculadora_gct():
    return render_template("calculadora_gct.html")

@app.route("/calculadora_pci", methods=['GET', 'POST'])
def calculadora_pci():
    return render_template("calculadora_pci.html")

@app.route("/calculadora_macros", methods=['GET', 'POST'])
def calculadora_macros():
    return render_template("calculadora_macros.html")

if __name__ == "__main__":
    app.run(debug=True)