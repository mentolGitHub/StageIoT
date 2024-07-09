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
from flask_restful import Api
from flask_cors import CORS
import base64


db : mysql.connector.MySQLConnection
db_cursor : mysql.connector.abstracts.MySQLCursorAbstract
app = Flask(__name__)
CORS(app)
api = Api(app)
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

def get_user_from_api_key(api_key):
    """
    Retrieve the username associated with the given API key.

    Args:
        api_key (str): The API key to be verified.

    Returns:
        str: The username associated with the API key if it is valid.
        None: If the API key is invalid or not found in the database.
    """
    query = "SELECT username FROM Users WHERE `api-key` = %s"
    db_cursor.execute(query, (api_key,))
    result = db_cursor.fetchall()
    if len(result) == 1:
        return result[0][0]
    else:
        return None


def hash_password(password):
    """
    Hashes the given password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.

    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def check_password(hashed_password, user_password):
    """
    Check if the provided user password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password stored in the database.
        user_password (str): The user's input password.

    Returns:
        bool: True if the user password matches the hashed password, False otherwise.
    """
    password_bytes = user_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)



@auth.verify_token
def verify_token(t):
    """
    Verify the authenticity of a token.

    Parameters:
    t (str): The token to be verified.

    Returns:
    bool: True if the token is valid, False otherwise.
    """
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
    """
    Error handler function for authentication errors.

    Parameters:
    - error: The error code.

    Returns:
    - A redirect response based on the error code.
    """
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
    """
    Checks if the user token is valid and returns the corresponding username.

    Returns:
        str: The username associated with the token if it is valid.
        None: If the token is invalid or not found in the database.
    """
    token = session.get('token')
    
    query = "SELECT user FROM Auth_Token WHERE token=%s"
    db_cursor.execute(query, (token,))
    res = db_cursor.fetchall()
    if db_cursor.rowcount==1:
        username = res[0][0]
        return username
    else:
        return None


@app.route('/')
def accueil():
    """
    Renders the index.html template with the appropriate variables.

    Returns:
        The rendered template with the 'is_authenticated' and 'username' variables.
    """
    is_authenticated = False
    username=''
    if session :
        is_authenticated = 'token' in session
        username = check_user_token()
    return render_template('index.html', is_authenticated=is_authenticated, username=username)



@app.route('/post_data', methods=['POST'])
def post_data():
    """
    Endpoint for receiving and processing data sent via POST request.
    
    Returns:
        JSON response: A JSON response indicating the status of the request.
    """
    if request.method == 'POST': 
        raw_data = request.get_data().decode('utf-8')
        raw_data= raw_data.removesuffix("\n")
        data_list = raw_data[1:].split(',')
        
        if int(raw_data[0]) == 2:
            if len(data_list) == 16:  # Assurez-vous que tous les champs attendus sont présents
                
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
                    "azimuth": float(data_list[14]),
                    "distance_recul": float(data_list[15])
                }
                
                Q_out.put(data)
                add_data_to_cache(data)         
                # print (data_storage)
                return jsonify({"status": "success"}), 200
            else:
                return jsonify({"status": "error", "message": "Invalid data format"}), 400
        else:
            return jsonify({"status": "error", "message": "Message ID not implemeneted yet"}), 400


def add_data_to_cache(data):
    """
    Add data to the cache based on the 'eui' value in the data dictionary.

    Parameters:
    - data (dict): The data to be added to the cache.

    Returns:
    - None
    """
    global data_storage
    if data['eui'] not in data_storage:
        data_storage[data['eui']] = [data]
    else:
        data_storage[data['eui']].append(data)
    # Supprimer les données de plus d'une heure
    for device in data_storage:
        seuil=0
        while (data_storage[device][-1]['timestamp']-data_storage[device][seuil]['timestamp'])/1000 > 61:
            seuil+=1

        data_storage[device]=data_storage[device][seuil:] 


@app.route('/get_data', methods=['GET'])
@auth.login_required
def get_data():
    """
        This function retrieves data from a MySQL database based on the provided parameters.

        Args:
            None

        Returns:
            A JSON response containing the retrieved data.

        Raises:
            None
    """
    duration = request.args.get('duration')
    
    db = mysql.connector.connect(host="localhost", user=Config["SQL_username"], database = Config["db_name"])
    cursor = db.cursor()
    username = check_user_token()
    query = "SELECT device FROM DeviceOwners WHERE owner = %s;"
    cursor.execute(query,(username,))
    result= cursor.fetchall()

    data = {}
    if len(result) !=0:
        for device in result[:][0]:
            if duration != None and float(duration) > 60:
                duration = float(duration)
                if (device in data_storage) and len(data_storage[device])>0:
                    args = (device,datetime.fromtimestamp(data_storage[device][-1]['timestamp']/1000-duration-1))
                else : 
                    args = (device,datetime.fromtimestamp(datetime.now().timestamp()-duration-1))
                
                query = "SELECT * FROM Data WHERE source= %s and timestamp > %s"
                cursor.execute(query,args)
                result = cursor.fetchall()
                data[device]=data_labels_to_json(result,"Data")
                
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

def data_labels_to_json(data,table):
    result = []
    db = mysql.connector.connect(host="localhost", user=Config["SQL_username"], database = Config["db_name"])
    cursor = db.cursor()
    query = "DESC "+table
    cursor.execute(query)
    desc = cursor.fetchall()
    label = [desc[i][0] for i in range(len(desc))]
    for d in data:
        mesure={}
        mesure['timestamp']=d[0].timestamp()*1000
        
        for i in range(1,len(d)-1):
            mesure[label[i]]=d[i]
        result.append(mesure)
    return result

@app.route('/get_euiList', methods=['GET', 'POST'])
@auth.login_required
def get_euiList():
    """
    Retrieves a list of eui associated with the logged-in user.

    Returns:
        A JSON response containing the list of devices eui.
    """
    username = session.get('username')
    query = "SELECT device FROM DeviceOwners WHERE owner = %s;"
    db_cursor.execute(query,(username,))
    result= db_cursor.fetchall()
    print(result)
    devices=[]
    length = len(result[:])
    if length != None and length > 0:
        for device in result[:][0]:
            query = "SELECT `dev-eui`, name FROM Device WHERE `dev-eui` = %s;"
            db_cursor.execute(query,(device,))
            devices.append(db_cursor.fetchall())
        print(devices[0])
        return jsonify(devices[0])  
    return jsonify([])



@app.route('/visualize')
@auth.login_required
def visualize():
    """
    Renders the visualize.html template.

    Returns:
        The rendered visualize.html template.
    """
    return render_template('visualize.html')



@app.route('/downloadall')
@auth.login_required
def downloadall():
    """
    Downloads all data from the data storage as a CSV file.

    Returns:
        Flask Response: Response object containing the CSV file as an attachment.
    """
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

@app.route('/download', methods=['GET', 'POST'])
def download():
    """
    Handle the download route for retrieving data from the database and generating a CSV file.

    Returns:
        Response: Flask response object containing the generated CSV file as an attachment.
    """
    if request.method == 'POST':
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        selected_fields = []
        for field in request.form.getlist('fields'):
            field = field.split(" ")
            for f in field:
                selected_fields.append(f)
        
        
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Function to handle user login.

    Deletes expired authentication tokens from the database.
    Validates the login form submitted by the user.
    Checks the username and password against the database records.
    Generates a new authentication token and stores it in the database.
    Sets the session variables for the logged-in user.
    Redirects the user to the home page if login is successful.
    Displays an error message if login is unsuccessful.

    Returns:
        If login is successful, redirects to the home page.
        If login is unsuccessful, renders the login page with an error message.
    """
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user.

    This function handles the registration process for a new user. It validates the registration form,
    checks if the username already exists in the database, and inserts the new user into the database
    if the username is unique. It also displays flash messages to indicate the status of the registration
    process and redirects the user to the appropriate page.

    Returns:
        A redirect response to the login page if the registration is successful, or the registration page
        with the registration form if there are validation errors or the username already exists.
    """
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


@app.route('/logout')
def logout():
    """
    Logs out the user by removing the 'username' and 'token' from the session.
    Displays a flash message to inform the user that they have been logged out.
    Redirects the user to the login page.
    """
    session.pop('username', None)
    session.pop('token')
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/map')
@auth.login_required
def map_view():
    """
    Renders the map view page.

    Returns:
        The rendered map.html template.
    """
    return render_template('map.html')


@app.route('/register_device', methods=['GET', 'POST'])
@auth.login_required
def register_device():
    """
    Register a device and associate it with a user.

    This function handles the registration of a device and its association with a user account.
    It first checks if the device is already registered. If not, it adds the device to the database
    and associates it with the currently logged-in user. If the device is already registered, it
    checks if it is already associated with the user. If not, it associates the device with the user.

    Returns:
        A redirect response to the 'register_device' page.

    """
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


@app.route('/deviceList')
@auth.login_required
def deviceList():
    """
    Retrieves the list of devices associated with the logged-in user.

    Returns:
        A rendered template 'deviceList.html' with the following variables:
        - username: The username of the logged-in user.
        - devices: A list of devices associated with the user.
        - names: A list of names corresponding to the devices.
        
    Redirects:
        - If the user is not logged in, redirects to the 'login' page.
    """
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
    


@app.route('/delete_device/<deveui>', methods=['GET', 'POST'])
@auth.login_required
def delete_device(deveui):
    """
    Deletes the device and its association with the user.

    Args:
        deveui (str): The device EUI to be deleted.

    Returns:
        redirect: A redirect response to the device list page.
    """
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

@app.route('/profile', methods=['GET', 'POST'])
@auth.login_required
def profile():
    """
    Displays the user profile page.

    Returns:
        The rendered profile.html template with the 'username' variable.
    """
    username=''
    if 'token' in session :
        username = check_user_token()


    return render_template('profile.html', username=username)

@app.route('/getApiKey', methods=['GET'])
@auth.login_required
def get_api_keys():
    username = ''
    if 'token' in session:
        username = check_user_token()

    query = "SELECT `api-key` FROM Users WHERE username = %s"
    db_cursor.execute(query, (username,))
    api_keys = db_cursor.fetchall()

    return jsonify(api_keys[0][0])

@app.route('/generateApiKey', methods=['GET', 'POST'])
@auth.login_required
def generate_api_key():
    username = ''
    if 'token' in session:
        username = check_user_token()

    # Générer une nouvelle clé API
    api_key = bcrypt.gensalt()
    # Convertir la clé API en une chaîne de caractères encodée en base64
    api_key_str = base64.b64encode(api_key).decode('utf-8')
    query = "UPDATE Users SET `api-key` = %s WHERE username = %s"
    db_cursor.execute(query, (api_key_str, username))
    db.commit()
    api_key = {"api_key": api_key_str}
    print(api_key)
    return jsonify(api_key)


"""==============================================================="""
"""                             API                               """
"""==============================================================="""

def get_user_from_api_key(api_key):
    """
    Retrieve the username associated with the given API key.

    Args:
        api_key (str): The API key to be verified.

    Returns:
        str: The username associated with the API key if it is valid.
        None: If the API key is invalid or not found in the database.
    """
    query = "SELECT username FROM Users WHERE `api-key` = %s"
    db_cursor.execute(query, (api_key,))
    result = db_cursor.fetchall()
    if len(result) == 1:
        return result[0][0]
    else:
        return None


@app.route('/api/deviceList', methods=['GET', 'POST'])
def apiDeviceList():
    """
    Retrieves a list of devices from the database.

    Returns:
        A JSON response containing the list of devices, where each device is represented as a dictionary with 'dev-eui' and 'name' keys.
    """
    key = request.args.get('key')
    username = get_user_from_api_key(key)
    query = """
    SELECT Device.`dev-eui`, Device.name 
    FROM Device
    JOIN DeviceOwners ON Device.`dev-eui` = DeviceOwners.device
    WHERE DeviceOwners.owner = %s
    """ 
    db_cursor.execute(query, (username,))
    devices = db_cursor.fetchall()
    
    result = [{"dev-eui": device[0], "name": device[1]} for device in devices]
    
    return jsonify(result)


@app.route('/api/deviceData/<deveui>', methods=['GET'])
def apiDevice_data(deveui):
    """
    Retrieve data from the 'Data' table based on the specified device EUI and time range.

    Args:
        deveui (str): The device EUI.

    Returns:
        flask.Response: A JSON response containing the retrieved data.

    """
    start_date = request.args.get('start_date', default=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'))
    end_date = request.args.get('end_date', default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    dataType = str(request.args.get('dataType', default='*'))
    print(dataType)

    if dataType in data_format.keys():
        select_clause = dataType
    elif dataType == "*":
        select_clause = "*"
    else:
        return jsonify({"error": "Invalid data type"})

    query = f"""
    SELECT {select_clause} FROM Data 
    WHERE source = %s AND timestamp BETWEEN %s AND %s
    ORDER BY timestamp DESC
    """
    db_cursor.execute(query, (deveui, start_date, end_date))
    data = db_cursor.fetchall()
    
    columns = [col[0] for col in db_cursor.description]
    result = [dict(zip(columns, row)) for row in data]
    
    return jsonify(result)

@app.route('/api/registerDevice', methods=['POST'])
def apiRegisterDevice():
    """
    
    """
    
    deveui = request.args.get('deveui')
    name = request.args.get('name')
    pwd = request.args.get('pwd')

    


@app.route('/api/neighbourList/<deveui>', methods=['GET'])
def apiNeighbourList(deveui):
    """
    Retrieves the list of neighboring sources based on the given device EUI.

    Args:
        deveui (str): The device EUI.

    Returns:
        list: A list of neighboring sources.

    """
    size = request.args.get('size', 0.001)

    query = "SELECT latitude, longitude FROM Data WHERE `source`=%s ORDER BY timestamp DESC LIMIT 1"
    db_cursor.execute(query, (deveui,))
    coords = db_cursor.fetchall()

    query = "SELECT DISTINCT `source` FROM Data WHERE abs(latitude - %s) < %s AND abs(longitude - %s)< %s AND timestamp > %s"
    db_cursor.execute(query, (coords[0][0], size, coords[0][1], size, (datetime.now() - timedelta(seconds=50)).strftime('%Y-%m-%d %H:%M:%S')))
    neighbours = db_cursor.fetchall()

    
    return jsonify(neighbours)



"""==============================================================="""
"""                          Lancement                            """
"""==============================================================="""


def IPnode(Q_output: Queue, config):
    """
    Starts the IP node server.

    Args:
        Q_output (Queue): The output queue for sending messages.
        config (dict): The configuration settings.

    Returns:
        None
    """
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


def IPnode_noconfig(Q_output: Queue):
    """
    Starts the IP node server without any configuration.

    Args:
        Q_output (Queue): The output queue for sending messages.

    Returns:
        None
    """
    global Q_out
    Q_out = Q_output
    
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context='adhoc')
    
if __name__ == '__main__':
    q = Queue()
    IPnode_noconfig(q)