from bottle import route, run, get, put
import time, Settings, json, subprocess

import firebase_admin
from firebase_admin import credentials, initialize_app
from firebase_admin import firestore
import subprocess, os


# Setup
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db=firestore.client()
print( "db initilied ... ")

#
# Main storage lists & Classes
#
settings = Settings
settingsString = '{ "max_amount_per_person" : 2, "max_household_size" : 2 }'
settingsJSON = json.loads(settingsString )

#app = Flask(__name__)

@put( '/offers' )
def put_offer():
    #sponsor_humanity_offer_amount = request.args.get('sponsor-humanity-offer-amount')
    #sponsor_humanity_uid = request.args.get('sponsor-humanity-uid')
    ts = int(time.time() * 1000)
    #print( "offer: amount= ", int(sponsor_humanity_offer_amount), ' uid= ', sponsor_humanity_uid )

    try:
        # cc_code = db.collection('offers').add({'offer_email': 'foo@foo.com'})
        #print( "cc code = ", cc_code )
        subprocess.run("python3 ./addoffer.py", shell=True )

        return( '200' )
    except Exception as e:    
        return f"An Error Occured: {e}"

@get( '/setting' )
def get_setting():
    #
    # read SETTING collection
    #
    print( 'Getting settings...')
    sdoc = db.collection('settings').document("SponsorHumanity").get()

    settings.max_amount =  sdoc.get("max_amount_per_person" )
    settings.max_household =  sdoc.get("max_household_size" )
    settings.max_number_vendors =  sdoc.get("max_number_vendors" ) 

    settingsJSON ["max_amount_per_person"] = settings.max_amount
    settingsJSON ["max_household_size"] = settings.max_household

    return( settingsJSON )


'''

        cc_code = db.collection('offers').add({'offer_email': 'foo@foo.com', 'phone':"999-999-9999", 
        'device_type': 'iPhone', 'serial_number': '1fyg2kkksa8',
        'offer_amount': int(sponsor_humanity_offer_amount), 
        'balance': int(sponsor_humanity_offer_amount), 
        'reserved': False, 'timestamp': ts,
        'uid' : sponsor_humanity_uid })
@app.route('/requests',methods = ['PUT'])
def put_request():
        int_1 = 1
        return( '200' )
'''

if __name__ == '__main__':
        run(host='localhost', port=5000, debug=True)