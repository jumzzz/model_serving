import os
from standard_payload import StandardPayload
from model_predict import Model
from redis_config import get_config

from flask import Flask, request
from flask_caching import Cache


ref_json = os.environ['REF_JSON']
transformer_file = os.environ['TRANSFORMER_FILE']
model_file = os.environ['MODEL_FILE'] 

std_payload = StandardPayload(ref_json=ref_json)
model = Model(model_file=model_file, transformer_file=transformer_file)

app = Flask(__name__)
cache = Cache(app, config=get_config())


@app.route('/predict_income', methods=['POST'])
@cache.cached(timeout=30, query_string=True)
def predict_income():
    payload = request.get_json()
    payload = std_payload.validate_data(payload)

    if payload['has_error']:
        return payload['error_msg']

    prediction = model.predict(payload['data'])
    return prediction


if __name__ == '__main__':
    app.run(host='0.0.0.0')

