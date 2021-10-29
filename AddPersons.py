import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import Settings

import time, json

# Setup with cert to SH firestore
# then add records to the collections
settings = Settings
settingsString = '{ "max_amount_per_person" : 2, "max_household_size" : 2 }'
settingsJSON = json.loads(settingsString )

def time_format():
    return f'{datetime.now()}|> '


cred = credentials.Certificate( "sponsor-humanity-firebase-adminsdk-s4a61-c20b26107e.json")
#cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

from datetime import datetime

sponsor_humanity_email = "jobo132017@gmail.com"

print( "serching person collection by email...")
docs = db.collection('person').where("email", "==", sponsor_humanity_email ).get()

#docs = db.collection('person').get()
#for doc in docs:
print(" # records =", len( docs), " ", )
for doc in docs:
    print( doc.to_dict()['is_anonymous'] ) 
    #print(doc.to_dict())

print( 'Getting settings...')
sdoc = db.collection('settings').get()
for doc in sdoc:
    print( doc.to_dict()['max_amount_per_person'] )
    print( doc.to_dict()['max_household_size'] ) 
    print( doc.to_dict())

print( sdoc.to_dict()['max_amount_per_person'] )
print( sdoc.to_dict()['max_household_size'] ) 

'''
settings.max_amount =  sdoc.get("max_amount_per_person" )
settings.max_household =  sdoc.get("max_household_size" )

settingsJSON ["max_amount_per_person"] = settings.max_amount
settingsJSON ["max_household_size"] = settings.max_household

settingsString = '<h1>Settings</h1> <p>Settings: max amount, household_size ' + \
        str(settings.max_amount) + ' ' + str(settings.max_household) + '</p>'
print ( settingsString )    

# add person

Each person’s profile is stored in the SH database, will have the following information.
    first_name:  (* required but not required for anonymous donor)
    last_name: (* required but not required for anonymous donor)
    email (unique): (* required but not required for anonymous donor)
    email_verified: (what type is this? bool?) (* required but not required for anonymous donor)
    display_name: (?)
    is_anonymous: (bool) - True for anonymous person (* required)
    photo_u_r_l: (link to photo ID or Null)
    house_size" null(for a donor), 1 to 4 (used in determining maximum request amount) (* required for requestor, not required for donor)
    phone: (with area code) (* required, but not required for an anonymous donor)
    vendor_card_preference: (“Walmart”, “Kroger”, “Publix”, “WholeFoods” (* required for requestor, not required for donor)
    status: active, pending (active is an authorized and default value) (* required)
    send_email_on_match: Bool (True for people that want email sent for a matching offer, otherwise False) (* required but not required for anonymous donor, default = True )
    uid: id of person in Authentication DB (* required but not required for anonymous donor, default = True )


      
db.collection('person').add ({  'first_name':'Lindsay', 'last_name':'Samuels', 'email': "lsamuels3@yahoo.com",
                                'email_verified': True, 'display_name': 'President Lindsay', 'is_anonymous': False,
                                'photo_u_r_l': '', 
                                'phone':'999-999-9990', 'house_size':1, 'vendor_card_preference':'Kroger',
                                'status': 'ACTIVE', 'send_email_on_match': True })
                               
db.collection('person').add ({  'first_name':'Clay', 'last_name':'Bogusky', 'email': 'jobo132017@gmail.com',
                                'email_verified': True, 'display_name': 'Vice President Clay', 'is_anonymous': False,
                                'photo_u_r_': '', 
                                'phone':'999-999-9991', 'house_size':2, 'vendor_preference':'Walmart',
                                'status': 'ACTIVE', 'send_email_on_match': True })

db.collection('person').add ({  'first_name':'David', 'last_name':'Seun', 'email': 'seundavid56@gmail.com',
                                'email_verified': True, 'display_name': 'King David', 'is_anonymous': False,
                                'photo_u_r_': '', 
                                'phone':'999-999-9992', 'house_size':4, 'vendor_preference':'Whole Foods',
                                'number_of_vendors_per_request':1, 'geopoint':'', 'phone_type':'iphone',
                                'status': 'ACTIVE', 'send_email_on_match': True })
'''
