from flask import Flask, jsonify, render_template, request
import requests

from block import Blockchain

# test

blockchain = Blockchain()

class API:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None):
        url = self.base_url + endpoint
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return 400

app = Flask(__name__)
api = API('http://127.0.0.1:5000')

@app.route("/")
def hello():
    data = api.get('/get_chain')
    return render_template('index.html', data=data)

@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/mining_block', methods=['POST'])
def mining_block():
    data = request.get_json()
    prev_block = blockchain.get_previous_block()
    prev_nonce = prev_block['nonce']
    nonce = blockchain.proof_of_work(prev_nonce)
    prev_hash = blockchain.hash(prev_block)
    block = blockchain.create_block(nonce, prev_hash, data)
    response = {
        'message': 'Congratulations, you just mined a block!',
        'new_block': {
            'index': block['index'],
            'timestamp': block['timestamp'],
            'nonce': block['nonce'],
            'previous_hash': block['previous_hash'],
            'data': block['data']
        }
    }
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(debug=True)