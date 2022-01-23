## Input Payload 

The endpoint `http://{args.host}/predict_income` accepts a post request which has a payload of json in this format


```
    {    
        "age": 90,
        "workclass": "?", 
        "fnlwgt": 77053,
        "education": "HS-grad",
        "marital.status": "Widowed",
        "occupation": "?", 
        "relationship": "Not-in-family",
        "race": "White",
        "sex": "Female",
        "capital.gain": 0,
        "capital.loss": 4356,
        "hours.per.week": 40,
        "native.country": "United-States"
    }

```

To send this with Python's `requests` library, just do

```
import requests

payload =  {    
        "age": 90,
        "workclass": "?", 
        "fnlwgt": 77053,
        "education": "HS-grad",
        "marital.status": "Widowed",
        "occupation": "?", 
        "relationship": "Not-in-family",
        "race": "White",
        "sex": "Female",
        "capital.gain": 0,
        "capital.loss": 4356,
        "hours.per.week": 40,
        "native.country": "United-States"
}

    
endpoint = f'http://{args.host}/predict_income'

req = requests.post(endpoint, json=payload)
result = req.json()

```

Which produces an output

```
{'predicted_income_class': '<=50k', 'prediction_raw': 0.07441679270879063, 'status': 'success'}
```

The file `payload_list.json`, contains a list of multiple payloads.


## Sending Sample Payload Locally

First, you have to make sure to run `docker-compose up -d` from `model_serving/` directory to ensure that the host is running.

To find the host you can run:

```
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

Here you'll find 

```
NAMES                   PORTS
model_serving_nginx_1   0.0.0.0:1337->80/tcp, :::1337->80/tcp
model_serving_web_1     5000/tcp
redis                   0.0.0.0:6379->6379/tcp, :::6379->6379/tcp
```

The host that binds model_serving_nginx_1 will be our host so let's use `0.0.0.0:1337` as our host.

Make sure that you also installed `requests` in your pip environment.

To start sending Payload to our local endpoint just run

```
python run_payload.py --host 0.0.0.0:1337 payload_list.json
```

This should produce an output

```
[1/100] Sending Payload: 
{'age': 90, 'workclass': '?', 'fnlwgt': 77053, 'education': 'HS-grad', 'marital.status': 'Widowed', 'occupation': '?', 
'relationship': 'Not-in-family', 'race': 'White', 'sex': 'Female', 'capital.gain': 0, 'capital.loss': 4356, 
'hours.per.week': 40, 'native.country': 'United-States'}

[1/100] Received response: 
{'predicted_income_class': '<=50k', 'prediction_raw': 0.07441679270879063, 'status': 'success'}


[2/100] Sending Payload: 
{'age': 82, 'workclass': 'Private', 'fnlwgt': 132870, 'education': 'HS-grad', 'marital.status': 'Widowed', 
'occupation': 'Exec-managerial', 'relationship': 'Not-in-family', 'race': 'White', 'sex': 'Female', 'capital.gain': 0, 
'capital.loss': 4356, 'hours.per.week': 18, 'native.country': 'United-States'}

[2/100] Received response: 
{'predicted_income_class': '<=50k', 'prediction_raw': 0.07441679270879063, 'status': 'success'}

...

```
