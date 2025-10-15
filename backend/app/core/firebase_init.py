import firebase_admin
from firebase_admin import credentials
import pyrebase
from dotenv import dotenv_values
env_values = dotenv_values('/.env')
api_key = env_values['GOOGLE_API_KEY']

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)

firebaseConfig = {
    "apiKey": api_key,
    "authDomain": "scholarmind-99228.firebaseapp.com",
    "projectId": "scholarmind-99228",
    "storageBucket": "scholarmind-99228.firebasestorage.app",
    "messagingSenderId": "51855942423",
    "appId": "1:51855942423:web:7594c01d745e0617a14d52",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)