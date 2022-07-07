import time
from datetime import timedelta
from uuid import uuid4
import firebase_admin
import os
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import firestore, initialize_app
from CRS_Evaluation.settings import SETTINGS_ROOT


class firebase_sdk:


    def __init__(self):
       if not firebase_admin._apps:
            file = os.path.join(SETTINGS_ROOT, 'firebase-SDK.json')
            cred = credentials.Certificate(file)
            firebase_admin.initialize_app(cred, {
                'databaseURL' :'https://infact.firebaseio.com'
            })




  # Initialize Firebase
#firebase.initializeApp(firebaseConfig);

