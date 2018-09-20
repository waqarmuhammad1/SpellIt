# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, request, json
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

def GetDictionaryFiles(data):
    print data
    return {"data":["Waqar", "Muhammad"]}

class dummy(Resource):
    def post(self):
        data1 = json.loads(request.data.decode())
        print data1
        lang_names = []
        with open('lang_names.txt', 'rb') as f:
            lang_names = f.readlines()
        lang_names = [x.split('\t')[1].replace('\n','') for x in lang_names if data1['lang'] in x.split('\t')[0]]
        if len(lang_names) > 0:
            lang_names = lang_names[0]

        print lang_names

        with open(lang_names+'.dic', 'rb') as f:
            dic_data = f.readlines()

        with open(lang_names+'.aff', 'rb') as f:
            affix_data = f.readlines()

        return {'dic': dic_data, 'affix': affix_data}

class GetLangNames(Resource):
    def post(self):
        with open('lang_names.txt', 'rb') as f:
            data =  f.readlines()
        data = [x.split('\t')[0] for x in data]

        data.remove('\n')

        return data


class SaveData(Resource):
    def post(self):

        data = json.loads(request.data.decode())

        lang_name = data['lang_name']
        lang_symb = data['lang_symbol']
        aff_data = data['aff_data']
        dic_data = data['dic_data']

        file_names = []
        with open('lang_names.txt', 'rb') as f:
            file_names = f.readlines()
        file_names = [x.split('\t')[0] for x in file_names]

        if lang_name in file_names:
            return {'Error': 'File name already exists please provide different file name'}

        with open('lang_names.txt', 'a+') as f:
            f.write('\n'+lang_name+'\t'+lang_symb)

        dic_file_name = lang_symb+'.dic'
        aff_file_name = lang_name+'.aff'
        if os.path.exists(dic_file_name):
            return {'Error': 'Dictionary file already exists with name "'+dic_file_name+'" please provide different name'}

        if os.path.exists(aff_file_name):
            return {'Error': 'Dictionary file already exists with name "'+aff_file_name+'" please provide different name'}

        with open(dic_file_name, 'wb') as f:
            f.writelines(dic_data)

        with open(aff_file_name, 'wb') as f:
            f.writelines(aff_data)


api.add_resource(dummy,'/dummy')
api.add_resource(SaveData,'/SaveData')
api.add_resource(GetLangNames,'/langs')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1',threaded = True)
