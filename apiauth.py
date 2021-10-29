#!/usr/bin/env python3.7
from flask import Flask, url_for, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth


import urllib3
import requests
import time 

app = Flask(__name__) 
from base64 import b64encode
username = 'sh_admin'
password = 'sh_password'
timestamp = time()
nonce = '654213'
encoded_credentials = b64encode(bytes(f'{username}:{password}',
                                encoding='ascii')).decode('ascii')
auth_header = f'Basic {encoded_credentials}'
# the auth_header above can now be used in our API request
# we'll look at that shortly

# just for testing, let's print the auth_header variable (this step will be removed later)
print(f'Auth header: {auth_header}')
