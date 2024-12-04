import requests
import json
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
from services import util


app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir requisições de outros domínios


@app.route('/doginder', methods=['GET'])
def register_get():
    return render_template('./index.html')


@app.route('/doginder', methods=['POST'])
def tinder():
    old_data = util.read_json('./data.json')
    user_id = request.json.get('user_id')
    animal_id = request.json.get('animal_id')
    is_liked = request.json.get('isLiked')
    if not util.is_present(old_data, user_id):
        util.insert_new_user(old_data, user_id)
    if is_liked:
        util.insert_in_user_liked(old_data, user_id, animal_id)
    else:
        util.insert_in_user_disliked(old_data, user_id, animal_id)
    with open('./data.json', 'w') as f:
        json.dump(old_data, f, indent=4)
    return jsonify({'message': 'Foi'})


if __name__ == '__main__':
    app.run(debug=True, port=3001)
