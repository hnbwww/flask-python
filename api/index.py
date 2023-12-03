from flask import Flask, render_template,jsonify, request
import requests
import json
import time
import os


app = Flask(__name__)



def fetch_data():
    try:
        response = requests.get('https://flask-python-lemon.vercel.app/get_qb?ID=QQDGSVIXBLDOWDHSTKKUCTOHDFRAZAXITNUHOJNWSACECKGUSGSTONPDZMDI')
        data = response.json()
        return data
    except Exception as e:
        print('Error fetching data:', e)
        return None

def calculate_total_diff(last_data, current_data):
    if last_data is None or current_data is None:
        return None, None

    last_solutions_found_total = sum(entry['solutionsFound'] for entry in last_data)
    last_current_its_total = sum(entry['currentIts'] for entry in last_data)
    current_solutions_found_total = sum(entry['solutionsFound'] for entry in current_data)
    current_current_its_total = sum(entry['currentIts'] for entry in current_data)

    solutions_diff = current_solutions_found_total - last_solutions_found_total
    its_diff = current_current_its_total - last_current_its_total
    lastActive = last_data[0].lastActive

    return lastActive,solutions_diff, its_diff

def save_current_data(data):
    with open('current_data.json', 'w') as file:
        json.dump(data, file)

def load_last_data():
    if os.path.exists('current_data.json'):
        with open('current_data.json', 'r') as file:
            return json.load(file)
    else:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diff')
def diff():
    last_data = load_last_data()
    current_data = fetch_data()
    
    if current_data:
        solutions_diff, its_diff = calculate_total_diff(last_data, current_data)
        if solutions_diff is not None and its_diff is not None:
            print(f'Total solutionsFound difference since last hour: {solutions_diff}')
            print(f'Total currentIts difference since last hour: {its_diff}')
        else:
            print('Failed to calculate differences.')

        save_current_data(current_data)
    pass
    
    return {'last_time':last_time,'solutions_diff': solutions_diff, 'its_diff': its_diff}

    

@app.route('/about')
def about():
    return 'About www'

@app.route('/get_qb')
def get_qb():
    qb_id = request.args.get('ID')
    if qb_id:
        url = f'https://api.qubic.li/PublicPool/Performance/{qb_id}'
        response = requests.get(url)

        if response.status_code == 200:
            qb_data = response.json()
            return jsonify(qb_data)
        else:
            return 'Failed to fetch QB data', response.status_code
    else:
        return 'Please provide an ID parameter for /get_qb route'

if __name__ == '__main__':
    app.run()
