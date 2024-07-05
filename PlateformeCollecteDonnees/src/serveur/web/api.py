from flask import Flask, jsonify, request, session
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, timedelta
from flask_httpauth import HTTPTokenAuth
import mysql.connector
import mysql.connector.abstracts

basic_auth = HTTPBasicAuth()
auth = HTTPTokenAuth(scheme='Bearer')
db : mysql.connector.MySQLConnection
db_cursor : mysql.connector.abstracts.MySQLCursorAbstract
Config = {}
app = Flask(__name__)

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

@app.route('/api/deviceList', methods=['GET', 'POST'])
@auth.login_required
def deviceList(self):
        print("device List")
        query = "SELECT `dev-eui`, name FROM Device"
        db_cursor.execute(query)
        devices = db_cursor.fetchall()
        
        result = [{"dev-eui": device[0], "name": device[1]} for device in devices]
        
        return jsonify(result)

@app.route('/api/device/<deveui>', methods=['GET', 'POST'])
@auth.login_required
def device_data(deveui):
    start_date = request.args.get('start_date', default=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'))
    end_date = request.args.get('end_date', default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    query = """
    SELECT * FROM Data 
    WHERE source = %s AND timestamp BETWEEN %s AND %s
    ORDER BY timestamp DESC
    """
    db_cursor.execute(query, (deveui, start_date, end_date))
    data = db_cursor.fetchall()
    
    columns = [col[0] for col in db_cursor.description]
    result = [dict(zip(columns, row)) for row in data]
    
    return jsonify(result)

def init_api(config, application):
    global Config
    global app
    Config = config
    app = application

