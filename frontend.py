from flask import Flask, request, render_template, jsonify
from utils import JsonDatabase, BackendCommunication

app = Flask(__name__)


# Route for handling GET requests
@app.route('/', methods=['GET'])
def get_data():
    message_database = JsonDatabase('messagesDatabase.json')
    data = message_database.read_from_json()
    return render_template('index.html', message=data)


# Route for handling POST requests
@app.route('/data', methods=['POST'])
def post_data():
    if request.headers.get('Content-Type') != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415
    try:
        data = request.get_json()
        message_database = JsonDatabase('messagesDatabase.json')
        bot_obj = BackendCommunication()
        message_database.write_json({
            'side': 'right',
            'message': data['message']
        })
        message_database.write_json({
            'side': 'left',
            'message': bot_obj.get_bot_response(data['message'])
        })
        response = {'message': {'side': bot_obj.get_bot_response(data['message'])}, 'data': data}
        return jsonify(response)
    except:
        return jsonify({'error': 'Invalid JSON data'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
