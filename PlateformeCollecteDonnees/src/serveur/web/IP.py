from queue import Queue
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session, flash
import io
import mysql.connector
import mysql.connector.abstracts
import csv
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
import bcrypt
from flask_httpauth import HTTPTokenAuth

def hash_password(password):
    # Convertir le mot de passe en bytes, générer un sel et hacher le mot de passe
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

def check_password(hashed_password, user_password):
    # Vérifier si le mot de passe fourni correspond au hachage
    password_bytes = user_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)


db : mysql.connector.MySQLConnection
db_cursor : mysql.connector.abstracts.MySQLCursorAbstract
app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')
app._static_folder = './static/'
app.secret_key = 'your_secret_key'
Q_out: Queue
data_storage = []  # List to store received data


# Verify token
@auth.verify_token
def verify_token(t):
    print(t)
    token=session.get('token')
    query = "SELECT * FROM Auth_Token WHERE token = %s AND `date-exp` > %s"
    db_cursor.execute(query, (token, datetime.now()))
    result = db_cursor.fetchall()
    return len(result) > 0

# Gestion des erreurs HTTP
@auth.error_handler
def unauthorized():
    flash('You must be logged in to view this page.', 'danger')
    return redirect(url_for('login'))
"""
    Index
"""
@app.route('/')
def accueil():
    is_authenticated = 'username' in session
    username = session.get('username', None)
    return render_template('index.html', is_authenticated=is_authenticated, username=username)


"""
    Gère la requête POST pour envoyer des données au serveur.
    
    Returns:
        - Si les données sont valides, renvoie un JSON avec le statut "success" et le code de statut 200.
        - Si les données sont invalides, renvoie un JSON avec le statut "error", le message "Invalid data format" et le code de statut 400.
"""
@app.route('/post_data', methods=['POST'])
def post_data():
    
    if request.method == 'POST':
        global data_storage
        raw_data = request.get_data().decode('utf-8')
        data_list = raw_data[1:].split(',')
        if len(data_list) == 15:  # Assurez-vous que tous les champs attendus sont présents
            data = {
                "eui": str(data_list[0]),
                "timestamp": int(data_list[1]),
                "latitude": float(data_list[2]),
                "longitude": float(data_list[3]),
                "altitude": float(data_list[4]),
                "luminosity": float(data_list[5]),
                "vitesse_angulaire_X": float(data_list[6]),
                "vitesse_angulaire_Y": float(data_list[7]),
                "vitesse_angulaire_Z": float(data_list[8]),
                "pressure": float(data_list[9]),
                "acceleration_X": float(data_list[10]),
                "acceleration_Y": float(data_list[11]),
                "acceleration_Z": float(data_list[12]),
                "angle": float(data_list[13]),
                "azimuth": float(data_list[14])
            }
            print(data)
            Q_out.put(data)
            data_storage.append(data)
            # Supprimer les données de plus d'une heure
            data_storage = [d for d in data_storage if d['timestamp']/1000 >= datetime.now().timestamp() - 62]
            # print (data_storage)
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid data format"}), 400

"""
    Envoi de données vers un appareil exterieur 

    Returns: Données au format json

    TODO : mettre des paramètes a la requete afin de pouvoir specifier les données demandées 
"""
@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(data_storage)  

"""
    Visualisation des données sous forme de courbes
"""
@app.route('/visualize')
@auth.login_required
def visualize():
    return render_template('visualize.html')


"""
    Télécharge toutes les données stockées au format CSV.

    Returns: Flask.Response: Réponse Flask contenant le fichier CSV en tant que pièce jointe.
"""
@app.route('/downloadall')
@auth.login_required
def downloadall():
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    header = ["timestamp", "latitude", "longitude", "altitude", "luminosity", 
              "vitesse_angulaire_X", "vitesse_angulaire_Y", "vitesse_angulaire_Z", 
              "pressure", "acceleration_X", "acceleration_Y", "acceleration_Z", 
              "angle", "azimuth"]
    writer.writerow(header)
    
    # Write data
    for data in data_storage:
        writer.writerow([data[field] for field in header])
    
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'iot_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

"""
    Permet d'acceder a une page de téléchargement des données ou l'on peut choisir quelles données l'on veut
    
    Returns: Les données demandées au format csv

    TODO : fix la page pour utiliser des requetes a la bdd
"""
@app.route('/download', methods=['GET', 'POST'])
@auth.login_required
def download():
    if request.method == 'POST':
        start_time = int(request.form.get('start_time', 0))
        end_time = int(request.form.get('end_time', 9999999999999))
        selected_fields = request.form.getlist('fields')

        filtered_data = [d for d in data_storage if start_time <= d['timestamp'] <= end_time]

        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(selected_fields)
        
        for data in filtered_data:
            writer.writerow([data.get(field, '') for field in selected_fields])
        
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'iot_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    else:
        all_fields = ["timestamp", "latitude", "longitude", "altitude", "luminosity", 
                      "vitesse_angulaire_X", "vitesse_angulaire_Y", "vitesse_angulaire_Z", 
                      "pressure", "acceleration_X", "acceleration_Y", "acceleration_Z", 
                      "angle", "azimuth"]
        return render_template('download.html', fields=all_fields)

# formulaire de login utilisateur
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=255)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# formulaire d'enregistrement d'un utilisateur
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=255)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# formulaire d'enregistrement d'un appareil
class DeviceRegistrationForm(FlaskForm):
    deveui = StringField('DevEUI', validators=[DataRequired(), Length(min=16, max=16)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

"""
    Page permettant de se connecter
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Recuperation des données rentrées dans le formulaire
        username = form.username.data
        password = form.password.data

        # Verification du username/password avec ce qui est enregistré dans la db
        query = "SELECT (password) FROM Users WHERE username = %s;"
        db_cursor.execute(query,(username,))
        result= db_cursor.fetchall()
        #print(result)
        if db_cursor.rowcount == 1:
            pwdhash=result[0][0].encode("utf-8")
            print(pwdhash)
            if check_password(pwdhash,password):
                session['username'] = username
                query = "INSERT INTO Auth_Token (token, user, `date-exp`) VALUES (%s, %s, %s)"
                token = bcrypt.gensalt()
                db_cursor.execute(query, (token, username, (datetime.now() + timedelta(hours=2))))
                db.commit()
                session['token']=token
                return redirect('/')
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

"""
    Page permettant de s'enregistrer'
"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Recuperation des données rentrées dans le formulaire
        username = form.username.data
        password = hash_password(form.password.data)

        # Verification du username pour éviter que 2 personnes aient le même
        query = "SELECT (username) FROM Users WHERE username = %s;"
        db_cursor.execute(query,(username,))
        result= db_cursor.fetchall()


        if len(result) > 0:
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        else:
            # Ajout a la base de donnée
            query = "INSERT INTO Users (username,password) VALUES (%s,%s)"
            db_cursor.execute(query,(username,password))
            db.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

"""
    Page permettant de se deconnecter
"""
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('token')
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

"""
    Visualisation des appareils sur une carte

    TODO : verifier si ca fonctionne avec plusieurs appareils et centrer la map sur l'appareil favori de l'utilisateur
"""
@app.route('/map')
@auth.login_required
def map_view():
    # if 'username' not in session:
    #     flash('Please log in to access this page', 'warning')
    #     return redirect(url_for('login'))
    return render_template('map.html')

"""
    Page permettant d'enregistrer un appareil
"""
@app.route('/register_device', methods=['GET', 'POST'])
@auth.login_required
def register_device():
    # if 'username' not in session:
    #     flash('Please log in to access this page', 'warning')
    #     return redirect(url_for('login'))
    form = DeviceRegistrationForm()
    if form.validate_on_submit():
        # Recuperation des données du formulaire
        deveui = form.deveui.data
        name = form.name.data
        password = hash_password(form.password.data)

        # Verifier si l'appareil existe déjà
        query = "SELECT `dev-eui` FROM Device WHERE `dev-eui` = %s;"
        db_cursor.execute(query, (deveui,))
        result = db_cursor.fetchall()
        if len(result) > 0:
            flash('Device already exists', 'danger')
            return redirect(url_for('register_device'))

        # Ajouter l'appareil a la base
        query = "INSERT INTO Device (`dev-eui`, name, password) VALUES (%s, %s, %s)"
        db_cursor.execute(query, (deveui, name, password))  # Ensure password is hashed
        db.commit()
        # Assicier un utilisateur à l'appareil
        username = session.get('username')
        if username:
            query = "INSERT INTO DeviceOwners (device, owner) VALUES (%s, %s)"
            db_cursor.execute(query, (deveui, username))
            db.commit()
            flash('Device added successfully', 'success')
            return redirect('/')
        else:
            flash('User not logged in', 'danger')
            return redirect(url_for('login'))

    return render_template('register_device.html', form=form)

"""
    Liste des Devices enregistrés
"""
@app.route('/deviceList')
@auth.login_required
def deviceList():
    # if 'username' not in session:
    #     flash('Please log in to access this page', 'warning')
    #     return redirect(url_for('login'))
    username = session.get('username')
    if username:
        #selectionner les appareils de l'utilisateur
        query = "SELECT `dev-eui` FROM DeviceOwners WHERE owner = %s"
        db_cursor.execute(query, (username,))
        devices = db_cursor.fetchall()
        return render_template('deviceList.html', username=username, devices=devices)
    else:
        flash('User not logged in', 'danger')
        return redirect(url_for('login'))
    

"""
    Supprimer un appareil
"""
@app.route('/delete_device/<deveui>', methods=['POST'])
@auth.login_required
def delete_device(deveui):
    # Supprimer la liaison entre l'appareil et l'utilisateur
    username = session.get('username')
    query = "DELETE * FROM DeviceOwners  WHERE (`dev-eui` = %s AND owner = %s)"
    db_cursor.execute(query, (deveui, username))

    # Supprimer l'appareil si aucun utilisateur n'est associé
    query = "SELECT * FROM DeviceOwners WHERE `dev-eui` = %s"
    db_cursor.execute(query, (deveui,))
    result = db_cursor.fetchall()
    if len(result) == 0:
        query = "DELETE * FROM Device WHERE `dev-eui` = %s"
        db_cursor.execute(query, (deveui,))

    return redirect(url_for('device_list'))


"""
    Lancement du serveur avec un fichier de configuration
"""
def IPnode(Q_output: Queue, config):
    global Q_out, db, db_cursor
    Q_out = Q_output
    db = db = mysql.connector.connect(host="localhost", user=config["SQL_username"])
    
    db_cursor = db.cursor()
    db_query = "USE "+ config["db_name"]
    db_cursor.execute(db_query)
    app.run(host=config['server_host'], port=int(config['server_port']), debug=False)

"""
    Lancement du serveur sans fichier de configuration
"""
def IPnode_noconfig(Q_output: Queue):
    global Q_out
    Q_out = Q_output
    
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')
    
if __name__ == '__main__':
    q = Queue()
    IPnode_noconfig(q)