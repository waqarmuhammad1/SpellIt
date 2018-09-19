# -*- coding: utf-8 -*-
from couchbase.cluster import Cluster, PasswordAuthenticator
import time


class CouchConnector():

    def __init__(self, username, password, ip):
        try:
            self.cluster = Cluster('couchbase://'+ip)
            self.cluster.authenticate(PasswordAuthenticator(username, password))

        except:
            print('poka')

    def Open_Bucket(self, bucket_name):
        self.bucket = self.cluster.open_bucket(bucket_name)

    def authenticate(self, username, password):
        try:
            print username
            print password
            pwd = self.bucket.get(username).value
            if pwd == password:
                return True
        except:
            raise Exception('Unkown username or password.')



    def StoreData(self, user, data):

        try:
            self.bucket.upsert(user, data)
            return True
        except:
            return False


