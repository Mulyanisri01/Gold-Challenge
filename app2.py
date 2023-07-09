import re
from flask import Flask, jsonify
from flask import Flask, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
#import library yang dibutuhkan
import pandas as pd
import numpy as np
import string
import nltk
import warnings
warnings.filterwarnings("ignore")
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


app2 = Flask(__name__)

# app2.json_encoder = LazyJSONEncoder
app2.json_provider_class = LazyJSONEncoder 
app2.json = LazyJSONEncoder(app2)

swagger_template = dict(
info={
    'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host = LazyString(lambda: request.host)
    
)

swagger_config= {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app2, template=swagger_template,
                  config=swagger_config)

@swag_from("docs/hello_world.yml", methods=['GET'])
@app2.route('/', methods=['GET'])
def hello_world():
    json_response = {
        'status code': 200,
        'description': "Menyapa Hello World",
        'data': "Hello World",
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_processing.yml", methods=['POST'])
@app2.route('/text-processing', methods=['POST'])
def text_processing():
    text = request.form.get('text')

    json_response = {
        'status code': 200,
        'description': "Teks yang sudah di proses",
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', text),
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/processing_file.yml", methods=['POST'])
@app2.route('/processing-file', methods=['POST'])
def processing_file():
    #upload file
    file = request.files.getlist('file')[0]

    #import file csv ke pandas
    df = pd.read_csv(file, encoding='ISO-8859-1')

    #ambil teks yang akan diproses dalam format list
    teks= df.text.to_list()

    #melakukan clensing pada teks
    cleansing = []
    for text in teks:
        cleansing.append(re.sub(r'[^a-zA-Z0-9]', ' ', text))
   
    json_response = {
        'status code': 200,
        'description': "Teks yang sudah di proses",
        'data': df.to_csv("Hasil_Preprocesing.csv"),
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    app2.run()