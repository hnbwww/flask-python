from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return 'About'

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
