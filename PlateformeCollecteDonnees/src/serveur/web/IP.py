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


db : mysql.connector.MySQLConnection
db_cursor : mysql.connector.abstracts.MySQLCursorAbstract
app = Flask(__name__)
app.secret_key = 'your_secret_key'
Q_out: Queue
data_storage = []  # List to store received data
users = {
    'user1': 'password1',
    'user2': 'password2'
}

@app.route('/')
def accueil():
    is_authenticated = 'username' in session
    username = session.get('username', None)
    return render_template('index.html', is_authenticated=is_authenticated, username=username)

@app.route('/post_data', methods=['POST'])
def post_data():
    if request.method == 'POST':
        global data_storage
        raw_data = request.get_data().decode('utf-8')
        data_list = raw_data[1:].split(',')
        if len(data_list) == 15:  # Ensure we have all expected fields
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
            #supprimmer des data de plus d'une heure
            data_storage = [d for d in data_storage if d['timestamp']/1000 >= datetime.now().timestamp() - 62]
            # print (data_storage)
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid data format"}), 400

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(data_storage)  

@app.route('/visualize')
def visualize():
    return render_template('visualize.html')


@app.route('/downloadall')
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

@app.route('/download', methods=['GET', 'POST'])
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

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data


        query = "SELECT (password) FROM Users WHERE username = %s;"
        db_cursor.execute(query,(username,))
        result= db_cursor.fetchall()
        if db_cursor.rowcount == 1:
            pwdhash=result[0][0]
            print(pwdhash)
            if password == pwdhash:
                session['username'] = username
                flash('Login successful', 'success')
                return redirect('/')
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        query = "SELECT (username) FROM Users WHERE username = %s;"
        db_cursor.execute(query,(username,))
        result= db_cursor.fetchall()
        if len(result) > 0:
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        else:
            query = "INSERT INTO Users (username,password) VALUES (%s,%s)"
            db_cursor.execute(query,(username,password))
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/map')
def map_view():
    if 'username' not in session:
        flash('Please log in to access this page', 'warning')
        return redirect(url_for('login'))
    return render_template('map.html')

@app.route('/register_device')
def register_device():
    if 'username' not in session:
        flash('Please log in to access this page', 'warning')
        return redirect(url_for('login'))
    return render_template('register_device.html')


def IPnode(Q_output: Queue, config):
    global Q_out, db, db_cursor
    Q_out = Q_output
    db = db = mysql.connector.connect(host="localhost", user=config["SQL_username"])
    
    db_cursor = db.cursor()
    db_query = "USE "+ config["db_name"]
    db_cursor.execute(db_query)
    app.run(host=config['server_host'], port=int(config['server_port']), debug=False)

def IPnode_noconfig(Q_output: Queue):
    global Q_out
    Q_out = Q_output
    
    app.run(host='0.0.0.0', port=5000, debug=True)
    
if __name__ == '__main__':
    q = Queue()
    IPnode_noconfig(q)