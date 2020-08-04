from flask import Flask, request, json
import boto3
import pickle

BUCKET_NAME = 'models-teamtwo'
MODEL_NAME = 'uk_change_estimator.sav'

app = Flask(__name__)

s3 = boto3.client('s3', region_name = 'eu-west-1')

@app.route('/', methods=['POST'])
def predict():

    body = request.get_json()
    data = body['data']

    model = load_model(MODEL_NAME)
    prediction = model.predict(data)

    result = {'prediction': prediction}

    return json.dump(result)

#get model from S3
def load_model(model_name):
    
    response = s3.get_object(Bucket=BUCKET_NAME, Key = model_name)

    model_str = response['Body'].read()
    model = pickle.load(model_str)

    return model

if __name__ == '__main__':
    app.run(host = '0.0.0.0')
