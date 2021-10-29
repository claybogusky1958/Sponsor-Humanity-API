from flask import Flask, redirect, url_for, request, jsonify
import time, Settings, subprocess

import firebase_admin
from firebase_admin import credentials, initialize_app
from firebase_admin import firestore
#from firebase import firebase  

import json

# Setup
#cred = credentials.Certificate("serviceAccountKey.json")
cred = credentials.Certificate( "sponsor-humanity-firebase-adminsdk-s4a61-c20b26107e.json")
firebase_admin.initialize_app(cred)

db=firestore.client()
print( "db initialized ... ")
#       
# Main storage lists & Classes
#
settings = Settings
settingsString = '{ "max_amount_per_person" : 2, "max_household_size" : 2 }'
settingsJSON = json.loads(settingsString )

app = Flask(__name__)
#app.config["DEBUG"] = True

@app.route('/requests',methods = ['PUT'])
def put_requests():
    sponsor_humanity_amount_requested = request.args.get('sponsor-humanity-requested-amount')
    sponsor_humanity_email = request.args.get('sponsor-humanity-requestor-email')
    sponsor_humanity_phone_number = request.args.get('sponsor-humanity-phone-number')  

    print( 'Getting settings for request...')
    sdoc = db.collection('settings').document("SponsorHumanity").get()
    settings.max_amount =  sdoc.get("max_amount_per_person" )
    settings.max_household =  sdoc.get("max_household_size" )
    print( "settings.max_household = ", settings.max_household, "settings.max_amount= ", settings.max_amount )
    
    ts = int(time.time() * 1000)
    print( "request: amount= ", int(sponsor_humanity_amount_requested), ' email= ', sponsor_humanity_email )

    # need to check person table for # of people in household using email address
    sdoc = db.collection('person').get()
    if ( len( sdoc ) == 0 ):
        print( "# person records = ", len(sdoc) )
        print( "User not found in person collection... ", sponsor_humanity_email )
        return( '400')
    
    counter = 0
    for doc in sdoc:
        counter += 1
        if ( doc.to_dict()['email'] == sponsor_humanity_email ):
            print( 'found email')
            if ( doc.to_dict()['is_anonymous'] == True ):
                print( "Anonymous user..." )
                return( '400')
            if ( doc.to_dict()['status'] != "ACTIVE" ):
                print( "Inactive person...")
                return( '400' )
            if doc.to_dict()['house_size'] is None:
                print( "house_size is NULL!")
                return( '400' )
            house_size = int(doc.to_dict()['house_size'])
            if ( house_size <= 0 ):
                print( "House Size is less than or = to 0 ...")
                return( '400' )
            break

    if (counter == len( sdoc )):
        print( "Email not found in person collection ... ", sponsor_humanity_email )
        return( '400' )

    if ( house_size >  settings.max_household  ):
        print( "House Size is greater than max_household_size in settings collection ...")
        return( '400' )    

    max_requested = int(settings.max_amount) * int( house_size )
    print( "Max amount requested = ", int(max_requested) )
    if ( int( sponsor_humanity_amount_requested ) < 25 ):
        print( 'put_requests(): amount requested < $25!!' )
        return( '400')   
    if ( int( sponsor_humanity_amount_requested ) > int(max_requested)  ):
        print( 'put_requests(): amount requested > max = ', max_requested )
        return( '400')   

    try:
        offer_command = "python3 ./addrequest.py " + sponsor_humanity_amount_requested + " " + sponsor_humanity_email + " " + sponsor_humanity_phone_number
        print( offer_command )
        result = subprocess.run( offer_command, shell=True )
        print( 'subprocess returned: ', result.returncode )
        if ( result.returncode != 0 ):
            return( '400' )
        else: 
            return( '200' )
        
    except Exception as e:
        f"put_requests(): Exception error Occured: {e}"
        return( '401' )

@app.route('/offers',methods = ['PUT'])
def put_offer():
    sponsor_humanity_offer_amount = request.args.get('sponsor-humanity-offer-amount')
    sponsor_humanity_uid = request.args.get('sponsor-humanity-uid')
    ts = int(time.time() * 1000)
    print( "offer: amount= ", int(sponsor_humanity_offer_amount), ' uid= ', sponsor_humanity_uid )

    if ( int( sponsor_humanity_offer_amount ) < 10 ): # lower limit for an offer
        return( '400')

    try:
        offer_command = "python3 ./addoffer.py " + sponsor_humanity_offer_amount + " " + sponsor_humanity_uid 
        print( offer_command )
        result = subprocess.run( offer_command, shell=True )
        print( 'subprocess returned: ', result.returncode )
        if ( result.returncode != 0 ):
            return( '400' )
        else: 
            return( '200' )
        
    except Exception as e:
        return f"An Error Occured: {e}"
        return( '401' )

@app.route('/setting', methods=['GET'])
def get_setting():
    #
    # read SETTING collection
    #
    print( 'Getting settings...')
    sdoc = db.collection('settings').document("SponsorHumanity").get()

    settings.max_amount =  sdoc.get("max_amount_per_person" )
    settings.max_household =  sdoc.get("max_household_size" )

    settingsJSON ["max_amount_per_person"] = settings.max_amount
    settingsJSON ["max_household_size"] = settings.max_household

    settingsString = '<h1>Settings</h1> <p>Settings: max amount, household_size' + \
            str(settings.max_amount) + ' ' + str(settings.max_household) + '</p>'
    print ( settingsString )
    return( settingsJSON )
    #return( settingsString )
    #return "<h1>Settings</h1><p>settingsString</p>"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'Welcome to the Sponsor Humanity API.' 

if __name__ == '__main__':
        app.run(debug = True)

