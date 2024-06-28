from queue import Queue
from flask import Flask, render_template, request, jsonify, send_file
import io
import csv
from datetime import datetime, timedelta

app = Flask(__name__)
Q_out: Queue
data_storage = []  # List to store received data

@app.route('/')
def accueil():
    return render_template('index.html')

@app.route('/post_data', methods=['POST'])
def post_data():
    if request.method == 'POST':
        global data_storage
        raw_data = request.get_data().decode('utf-8')
        data_list = raw_data[1:].split(',')
        if len(data_list) == 14:  # Ensure we have all expected fields
            data = {
                "timestamp": int(data_list[0]),
                "latitude": float(data_list[1]),
                "longitude": float(data_list[2]),
                "altitude": float(data_list[3]),
                "luminosity": float(data_list[4]),
                "vitesse_angulaire_X": float(data_list[5]),
                "vitesse_angulaire_Y": float(data_list[6]),
                "vitesse_angulaire_Z": float(data_list[7]),
                "pressure": float(data_list[8]),
                "acceleration_X": float(data_list[9]),
                "acceleration_Y": float(data_list[10]),
                "acceleration_Z": float(data_list[11]),
                "angle": float(data_list[12]),
                "azimuth": float(data_list[13])
            }
            print(data)
            Q_out.put(data)
            data_storage.append(data)
            #supprimmer des data de plus d'une heure
            data_storage = [d for d in data_storage if d['timestamp']/1000 >= datetime.now().timestamp() - 62]
            print (data_storage)
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

def IPnode(Q_output: Queue, config):
    global Q_out
    Q_out = Q_output
    app.run(host='0.0.0.0', port=5000, debug=True)
    
if __name__ == '__main__':
    q = Queue()
    IPnode(q, None)