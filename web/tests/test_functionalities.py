"""
Use: python -m pytest ../tests/test_functionalities.py -v
"""

from standard_payload import StandardPayload
from model_predict import Model
from utils import load_json

import os

REF_JSON = 'dependencies/standard_payload.json'
TRANSFORMER_FILE = 'dependencies/data_transformer.pkl'
MODEL_FILE = 'dependencies/model.txt'


TEST_DATA_DIR = '../tests/test_files'
PAYLOAD_VALID = 'payload_valid.json'
PAYLOAD_EXCESS = 'payload_excess.json'
PAYLOAD_INVALID_CATEGORY = 'payload_invalid_category.json'
PAYLOAD_INVALID_DTYPE = 'payload_invalid_dtype.json'
PAYLOAD_MISSING = 'payload_missing.json'
PAYLOAD_NEGATIVE = 'payload_negative.json'


def test_valid_payload():

    payload_path = os.path.join(TEST_DATA_DIR, PAYLOAD_VALID)
    
    payload = load_json(payload_path)
    std_payload = StandardPayload(ref_json=REF_JSON)
    validated = std_payload.validate_data(payload)

    assert not validated['has_error'], 'test_valid_payload fail'


def test_excess():

    payload_path = os.path.join(TEST_DATA_DIR, PAYLOAD_EXCESS)
    
    payload = load_json(payload_path)
    std_payload = StandardPayload(ref_json=REF_JSON)
    validated = std_payload.validate_data(payload)

    has_excess_key = 'ocean' in payload
    excess_key_removed = 'ocean' not in validated['data']

    assert has_excess_key and excess_key_removed, 'test_excess fail'


def test_invalid_category():

    payload_path = os.path.join(TEST_DATA_DIR, PAYLOAD_INVALID_CATEGORY)
    
    payload = load_json(payload_path)
    std_payload = StandardPayload(ref_json=REF_JSON)
    validated = std_payload.validate_data(payload)

    assert validated['error_msg']['error_type'] == 'invalid_categorical_data', 'test_invalid_category fail'


def test_invalid_dtype():

    payload_path = os.path.join(TEST_DATA_DIR, PAYLOAD_INVALID_DTYPE)
    
    payload = load_json(payload_path)
    std_payload = StandardPayload(ref_json=REF_JSON)
    validated = std_payload.validate_data(payload)

    assert validated['error_msg']['error_type'] == 'invalid_data_type', 'test_invalid_dtype fail'


def test_missing():

    payload_path = os.path.join(TEST_DATA_DIR, PAYLOAD_MISSING)
    
    payload = load_json(payload_path)
    std_payload = StandardPayload(ref_json=REF_JSON)
    validated = std_payload.validate_data(payload)

    assert validated['error_msg']['error_type'] == 'missing_fields', 'test_missing fail'


def test_negative():

    payload_path = os.path.join(TEST_DATA_DIR, PAYLOAD_NEGATIVE)
    
    payload = load_json(payload_path)
    std_payload = StandardPayload(ref_json=REF_JSON)
    validated = std_payload.validate_data(payload)

    assert validated['error_msg']['error_type'] == 'fields_with_negative', 'test_negative fail'


def test_model_predict():

    model = Model(model_file=MODEL_FILE, 
                 transformer_file=TRANSFORMER_FILE)

    payload_path = os.path.join(TEST_DATA_DIR, PAYLOAD_VALID)
    
    payload = load_json(payload_path)
    std_payload = StandardPayload(ref_json=REF_JSON)
    payload = std_payload.validate_data(payload)

    result = model.predict(payload['data'])

    val1 = result['status'] == 'success'
    val2 = result['predicted_income_class'] == '<=50k' or result['predicted_income_class'] == '>50k'
    val3 = result['prediction_raw'] >= 0

    assert val1 and val2 and val3, 'test_model_predict fails'

    








