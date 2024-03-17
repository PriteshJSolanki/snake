from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def get_data():
    # Get the data sent from the client
    data = request.get_json()

    # Do something with the data here...

    # Send some data back to the client
    return jsonify({"message": "Data received, Motherfucker!! Now do something with it!", "received_data": data})

if __name__ == '__main__':
    app.run(debug=True)
