# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, request, json
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from aeroSpike import CouchConnector

app = Flask(__name__)
CORS(app)
api = Api(app)


class AuthenticateUser(Resource):
    def post(self):
        data = json.loads(request.data.decode())
        username = data['user']
        password = data['pass']
        couch = CouchConnector('Administrator', 'password', 'localhost')
        couch.Open_Bucket('auth')
        result = couch.authenticate(username, password)

        if result == True:
            global user
            global pwd
            user = username
            pwd = password
            print user
            print pwd
        return result

class GetCurrentUser(Resource):
    def post(self):
        return user


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

        response = json.loads(request.data.decode())

        meta = response['meta']
        data = response['data']
        print(response)
        dictionary = {}
        for x in data:
            root_words = filter(None,x['root_data'].split('\n'))
            print(root_words)
            dictionary[x['root_word']] = root_words
        print user
        print pwd
        final_data = {"lang_name":meta['lang_name'], 'lang_symbol': meta['lang_symbol'], 'words_data':dictionary}
        couch = CouchConnector('Administrator', 'password', 'localhost')
        couch.Open_Bucket('auth')

        result = couch.authenticate(user, pwd)
        if result == True:
            couch.Open_Bucket('data')
            username = meta['user']
            couch.StoreData(username, final_data)





user = ''
pwd = ''

api.add_resource(GetCurrentUser,'/get_user')
api.add_resource(AuthenticateUser,'/auth')
api.add_resource(dummy,'/dummy')
api.add_resource(SaveData,'/save_data')
api.add_resource(GetLangNames,'/langs')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1',threaded = True)
