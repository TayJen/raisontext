import pickle

from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from

from raisontext import config

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/predict', methods=['POST'])
@swag_from({
    'tags': ['predict'],
    'parameters': [{
        'name': 'texts',
        'in': 'body',
        'description': 'List of texts',
        'required': True,
        'type': 'array',
        'items': {
            'type': 'string'
        }
    }],
    'responses': {
        200: {
            'description': 'List of predcited probabilities of whether a text was generated with LLM',
            'examples': {
                'application/json': {
                    'results': [0.1, 0.2, 0.3]
                }
            }
        }
    }
})
def predict():
    """Endpoint that returns predicted probabilities of whether a text was generated with LLM"""
    texts = request.json.get('texts', [])

    MODELS_DIR = config.REPO_ROOT / 'models'
    model_dir = MODELS_DIR / 'TfIdfLogReg_first silly baseline'
    model_name = '4a015324-601a-43d3-9df9-856323b97f0d.pkl'
    with open(model_dir / model_name, 'rb') as f:
        model = pickle.load(f)

    predictions = model.predict(texts)

    return jsonify({'results': predictions})


if __name__ == '__main__':
    app.run(debug=True)
