from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/tensorflow', methods=['POST'])
def tensorflow_endpoint():
    data = request.json
    # Aquí procesarías el dato con tu modelo TensorFlow
    # Por ahora solo lo devolvemos como está
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000)
