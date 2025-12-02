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


@app.route("/registro_datos", methods=["GET", "POST"])
def registro_datos():
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
        
        if email in emails:
            flash("Ya existe una cuenta con este email")
            return render_template("registro_datos.html")
        
        if password != confirm_password:
            flash("Las contraseñas no son iguales")
            return render_template("registro_datos.html")
        
        session['registro_datos'] = {
            'name': name,
            'lastname': lastname,
            'birthdate': f"{day}/{month}/{year}",
            'gender': gender,
            'email': email,
            'password': password
        }
        
        return redirect(url_for('registro_personal'))
    
    return render_template("registro_datos.html")

@app.route("/registro_personal", methods=["GET", "POST"])
def registro_personal():
    if 'registro_datos' not in session:
        return redirect(url_for('registro_datos'))
    
    if request.method == "POST":
        biological_sex = request.form.get("sexo")
        weight = request.form.get("peso")
        height = request.form.get("altura")
        activity_level = request.form.get("nivel_actividad")
        goal = request.form.get("objetivo")
        cooking_exp = request.form.get("nivel_experiencia")
        
        session['registro_personal'] = {
            'biological_sex': biological_sex,
            'weight': weight,
            'height': height,
            'activity_level': activity_level,
            'goal': goal,
            'cooking_exp': cooking_exp
        }
        
        return redirect(url_for('registro_preferencias'))
    
    return render_template("registro_personal.html")

@app.route("/registro_preferencias", methods=["GET", "POST"])
def registro_preferencias():
    if 'registro_datos' not in session or 'registro_personal' not in session:
        return redirect(url_for('registro_datos'))
    
    if request.method == "POST":
        allergies = request.form.get("alergias")
        intolerances = request.form.get("intolerancias")
        diet = request.form.get("dieta")
        disliked_foods = request.form.get("alimentos_no_gustan")
        
        datos = session['registro_datos']
        personal = session['registro_personal']
        
        email = datos['email']
        emails.append(email)
        users[email] = {
            **datos,
            **personal,
            'allergies': allergies,
            'intolerances': intolerances,
            'diet': diet,
            'disliked_foods': disliked_foods
        }
        
        session.pop('registro_datos', None)
        session.pop('registro_personal', None)
        
        global current_user
        current_user = email
        
        flash('¡Usuario registrado exitosamente!')
        return redirect(url_for('cuenta'))
    
    return render_template("registro_preferencias.html")

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

@app.route("/acerca_de")
def acerca_de():
    return render_template("acerca_de.html")

@app.route("/calculadoras")
def calculadoras():
    return render_template("calculadoras.html")

@app.route("/calculadora_imc", methods=['GET', 'POST'])
def calculadora_imc():
    imc = None
    categoria = None
    
    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        
        imc = round(peso / (altura * altura), 1)
        
        if imc < 18.5:
            categoria = "Bajo peso"
        elif imc < 25:
            categoria = "Normal"
        elif imc < 30:
            categoria = "Sobrepeso"
        else:
            categoria = "Obesidad"
    
    return render_template("calculadora_imc.html", imc=imc, categoria=categoria)

@app.route("/calculadora_tmb", methods=['GET', 'POST'])
def calculadora_tmb():
    tmb = None
    
    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        edad = int(request.form['edad'])
        sexo = request.form['sexo']
        
        if sexo == 'masculino':
            tmb = round(10 * peso + 6.25 * altura - 5 * edad + 5, 1)
        else:
            tmb = round(10 * peso + 6.25 * altura - 5 * edad - 161, 1)
    
    return render_template("calculadora_tmb.html", tmb=tmb)

@app.route("/calculadora_gct", methods=['GET', 'POST'])
def calculadora_gct():
    gct = None
    
    if request.method == 'POST':
        tmb = float(request.form['tmb'])
        actividad = float(request.form['actividad'])
        
        gct = round(tmb * actividad, 1)
    
    return render_template("calculadora_gct.html", gct=gct)

@app.route("/calculadora_pci", methods=['GET', 'POST'])
def calculadora_pci():
    pci = None
    
    if request.method == 'POST':
        altura = float(request.form['altura'])
        sexo = request.form['sexo']
        
        if sexo == 'masculino':
            pci = round(altura - 100 - ((altura - 150) / 4), 1)
        else:
            pci = round(altura - 100 - ((altura - 150) / 2.5), 1)
    
    return render_template("calculadora_pci.html", pci=pci)

@app.route("/calculadora_macros", methods=['GET', 'POST'])
def calculadora_macros():
    macros = None
    
    if request.method == 'POST':
        calorias = int(request.form['calorias'])
        objetivo = request.form['objetivo']
        
        if objetivo == 'mantener':
            # 30% proteínas, 40% carbohidratos, 30% grasas
            prot_pct, carb_pct, grasa_pct = 0.30, 0.40, 0.30
        elif objetivo == 'perder':
            # 35% proteínas, 35% carbohidratos, 30% grasas
            prot_pct, carb_pct, grasa_pct = 0.35, 0.35, 0.30
        else:  # ganar
            # 25% proteínas, 45% carbohidratos, 30% grasas
            prot_pct, carb_pct, grasa_pct = 0.25, 0.45, 0.30
        
        cal_proteinas = round(calorias * prot_pct)
        cal_carbohidratos = round(calorias * carb_pct)
        cal_grasas = round(calorias * grasa_pct)
        
        macros = {
            'proteinas': round(cal_proteinas / 4, 1),
            'carbohidratos': round(cal_carbohidratos / 4, 1),
            'grasas': round(cal_grasas / 9, 1),
            'calorias_proteinas': cal_proteinas,
            'calorias_carbohidratos': cal_carbohidratos,
            'calorias_grasas': cal_grasas
        }
    
    return render_template("calculadora_macros.html", macros=macros)

if __name__ == "__main__":
    app.run(debug=True)