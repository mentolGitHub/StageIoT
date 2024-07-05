from queue import Queue
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session, flash, Request
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
from pydoc import locate

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
data_storage = {}
Config = {}
data_format = { 'timestamp':"", 'luminosity':None, 'pression':None, 'temperature':None,
                'longitude':None, 'latitude':None, 'altitude':None, 'angle':None, 
                'vitesse_angulaire_X':None, 'vitesse_angulaire_Y':None, 'vitesse_angulaire_Z':None,
                'acceleration_X':None, 'acceleration_Y':None, 'acceleration_Z':None,
                'azimut':None, 'distance_recul':None, 'presence':None , 'humidite':None }

# Verify token
@auth.verify_token
def verify_token(t):
    # print(t)
    db = mysql.connector.connect(host="localhost", user=Config["SQL_username"], database = Config["db_name"])
    cursor = db.cursor()
    token=session.get('token')
    query = "SELECT * FROM Auth_Token WHERE token = %s AND `date-exp` > %s"
    cursor.execute(query, (token, datetime.now()))
    result = cursor.fetchall()
    return len(result) > 0

# Gestion des erreurs HTTP
@auth.error_handler
def err_handler(error):
    match (error):
        case 401 :
            flash('You must be logged in to view this page.', 'danger')
            return redirect(url_for('login'))
        case 404 :
            return redirect(url_for('/'))
        case 302 :
            flash('You must be logged in to view this page.', 'danger')
            return redirect(url_for('login'))


def check_user_token():
    token = session.get('token')
    
    query = "SELECT user FROM Auth_Token WHERE token=%s"
    db_cursor.execute(query, (token,))
    res = db_cursor.fetchall()[0][0]
    if db_cursor.rowcount==1:
        username = res
        return username
    else:
        return None

"""
    Index
"""
@app.route('/')
def accueil():
    is_authenticated = False
    username=''
    if session :
        is_authenticated = 'token' in session
        username = check_user_token()
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
        if int(raw_data[0]) == 2:
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
                # print(data)
                Q_out.put(data)
                if data_list[0] not in data_storage:
                    data_storage[data_list[0]] = [data]
                else:
                    data_storage[data_list[0]].append(data)
                # Supprimer les données de plus d'une heure
                for device in data_storage:
                    seuil=0
                    while (data_storage[device][-1]['timestamp']-data_storage[device][seuil]['timestamp'])/1000 > 61:
                        seuil+=1

                    data_storage[device]=data_storage[device][seuil:]                  
                # print (data_storage)
                return jsonify({"status": "success"}), 200
            else:
                return jsonify({"status": "error", "message": "Invalid data format"}), 400
        else:
            return jsonify({"status": "error", "message": "Message ID not implemeneted yet"}), 400


"""
    Envoi de données vers un appareil exterieur 

    Returns: Données au format json

    TODO : mettre des paramètes a la requete afin de pouvoir specifier les données demandées 
"""
@app.route('/get_data', methods=['GET'])
@auth.login_required
def get_data():
    duration = request.args.get('duration')
    champs = request.args.get('field')

    
    db = mysql.connector.connect(host="localhost", user=Config["SQL_username"], database = Config["db_name"])
    cursor = db.cursor()
    username = check_user_token()
    query = "SELECT device FROM DeviceOwners WHERE owner = %s;"
    cursor.execute(query,(username,))
    result= cursor.fetchall()

    

    data = {}
    if len(result) !=0:
        query = "DESC Data"
        cursor.execute(query)
        desc = cursor.fetchall()
        labels = [desc[i][0] for i in range(len(desc))]
        for device in result[:][0]:
            if duration != None and float(duration) > 60:
                duration = float(duration)
                
                
                
                # print(types)
                if (device in data_storage) and len(data_storage[device])>0:
                    args = (device,datetime.fromtimestamp(data_storage[device][-1]['timestamp']/1000-duration-1))
                else : 
                    args = (device,datetime.fromtimestamp(datetime.now().timestamp()-duration-1))
                
                query = "SELECT * FROM Data WHERE source= %s and timestamp > %s"
                cursor.execute(query,args)
                # print(args)
                result = cursor.fetchall()
                # print(result)
                data[device]=[]
                for d in result:
                    mesure={}
                    mesure['timestamp']=d[0].timestamp()*1000
                    
                    for i in range(1,len(d)-1):
                        mesure[labels[i]]=d[i]
                    
                    data[device].append(mesure)
                
            else:
                data[device]=[]
                if device in data_storage:
                    if duration != None:
                        duration = float(duration)
                        info = data_storage[device]
                        seuil = 0
                        # print(info)
                        while (info[-1]['timestamp']-info[seuil]['timestamp'])/1000 > duration+1:
                            seuil+=1
                        data[device]+=info[seuil:]
                    else :
                        data[device]+=data_storage[device]
    # print(data)
    return jsonify(data) 

@app.route('/get_euiList', methods=['GET', 'POST'])
@auth.login_required
def get_euiList():
    username = session.get('username')
    query = "SELECT device FROM DeviceOwners WHERE owner = %s;"
    db_cursor.execute(query,(username,))
    result= db_cursor.fetchall()
    print(result)
    devices=[]
    for device in result[:][0]:
        query = "SELECT `dev-eui`, name FROM Device WHERE `dev-eui` = %s;"
        db_cursor.execute(query,(device,))
        devices.append(db_cursor.fetchall())
    print(devices[0])
    return jsonify(devices[0])  


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
    for device_id, datas in data_storage.items():
        for data in datas:
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
def download():
    if request.method == 'POST':
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        selected_fields = request.form.getlist('fields')

        # Convert datetime-local input to datetime object
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')

        # Retrieve data from the database based on the selected criteria
        query = f"SELECT {', '.join(selected_fields)} FROM Data WHERE timestamp BETWEEN %s AND %s"
        db_cursor.execute(query, (start_time, end_time))
        data = db_cursor.fetchall()

        # Generate CSV file
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(selected_fields)
        print (data)
        for row in data:
            print (row)
            writer.writerow(row)
        output.seek(0)

        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'data_{start_time.strftime("%Y%m%d_%H%M%S")}_to_{end_time.strftime("%Y%m%d_%H%M%S")}.csv'
        )
    
    return render_template('download.html')

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
class DeviceAssociationForm(FlaskForm):
    deveui = StringField('DevEUI', validators=[DataRequired(), Length(min=16, max=16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    submit = SubmitField('Associate')


# formulaire d'enregistrement d'un appareil
class DeviceRegistrationForm(FlaskForm):
    deveui = StringField('DevEUI', validators=[DataRequired(), Length(min=16, max=16)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit2 = SubmitField('Register')

"""
    Page permettant de se connecter
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    query = "DELETE FROM Auth_Token WHERE `date-exp` < %s "
    db_cursor.execute(query,(datetime.now(),))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Recuperation des données rentrées dans le formulaire
        username = form.username.data
        password = form.password.data
        db_cursor.fetchall()
        # Verification du username/password avec ce qui est enregistré dans la db
        query = "SELECT (password) FROM Users WHERE username = %s;"
        db_cursor.execute(query,(username,))
        result= db_cursor.fetchall()
        # print(result)
        if db_cursor.rowcount == 1:
            pwdhash=result[0][0].encode("utf-8")
            # print(pwdhash)
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
    form_associate = DeviceAssociationForm()
    if form_associate.submit.data and form_associate.validate():
        deveui = form_associate.deveui.data
        password = hash_password(form_associate.password.data)
        query = "SELECT `dev-eui` FROM Device WHERE `dev-eui` = %s;"
        db_cursor.execute(query, (deveui,))
        # print("nb trouvé :"+str(db_cursor.rowcount))
        if len(db_cursor.fetchall())==1:
            username = check_user_token()
            if username:
                query = "SELECT * FROM DeviceOwners WHERE device = %s AND owner=%s"
                db_cursor.execute(query, (deveui, username))
                if len(db_cursor.fetchall())>0:
                    flash('Device already linked to account', 'danger')
                    return redirect(url_for('register_device'))
                query = "INSERT INTO DeviceOwners (device, owner) VALUES (%s, %s)"
                db_cursor.execute(query, (deveui, username))
                db.commit()
                flash('Device added successfully', 'success')
                return redirect(url_for('register_device'))
            else:
                flash('User not logged in', 'danger')
                return redirect(url_for('login'))
        else :
            flash('This device is not registered yet', 'danger')
            return redirect(url_for('register_device'))

    form = DeviceRegistrationForm()
    if form.submit2.data and form.validate():
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

        # TODO: Ajout a TTN via http ou via l'api
        # appid="stm32lora1"
        # requests.post(Config['APP_hostname']+"/applications/"+appid+"/devices/"+deveui)

        # Assicier un utilisateur à l'appareil
        username = check_user_token()
        if username:
            query = "INSERT INTO DeviceOwners (device, owner) VALUES (%s, %s)"
            db_cursor.execute(query, (deveui, username))
            db.commit()
            flash('Device added successfully', 'success')
            return redirect(url_for('register_device'))
        else:
            flash('User not logged in', 'danger')
            return redirect(url_for('login'))

    return render_template('register_device.html', form_associate=form_associate, form=form)

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
        query = "SELECT `device` FROM DeviceOwners WHERE owner = %s"
        db_cursor.execute(query, (username,))
        devices = db_cursor.fetchall()
        names = []
        for i in devices:
            # print(i)
            query = "SELECT name FROM Device WHERE `dev-eui` = %s"
            db_cursor.execute(query, i)
            names += [j[0] for j in db_cursor.fetchall()]
        
            #clement
        devices = [i[0] for i in devices]
        return render_template('deviceList.html', username=username, devices=devices, names = names)
    else:
        flash('User not logged in', 'danger')
        return redirect(url_for('login'))
    

"""
    Supprimer un appareil
"""
@app.route('/delete_device/<deveui>', methods=['GET', 'POST'])
@auth.login_required
def delete_device(deveui):
    # Supprimer la liaison entre l'appareil et l'utilisateur
    username = session.get('username')
    query = "DELETE FROM DeviceOwners WHERE device = %s AND owner = %s"
    db_cursor.execute(query, (deveui, username))
    db.commit()

    # Supprimer l'appareil si aucun utilisateur n'est associé
    query = "SELECT * FROM DeviceOwners WHERE `device` = %s"
    db_cursor.execute(query, (deveui,))
    result = db_cursor.fetchall()
    if len(result) == 0:
        query = "DELETE FROM Device WHERE `dev-eui` = %s"
        db_cursor.execute(query, (deveui,))
        db.commit()

    return redirect(url_for('deviceList'))


"""
    Lancement du serveur avec un fichier de configuration
"""
def IPnode(Q_output: Queue, config):
    global Q_out, db, db_cursor, Config
    Config= config
    Q_out = Q_output
    db = mysql.connector.connect(host="localhost", user=config["SQL_username"])
    app.app_context().push()
    with app.app_context():
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