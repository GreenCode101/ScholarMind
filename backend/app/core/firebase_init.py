import firebase_admin
from firebase_admin import credentials
import pyrebase

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)

firebaseConfig = {
    "apiKey": "",
    "authDomain": "scholarmind-99228.firebaseapp.com",
    "projectId": "scholarmind-99228",
    "storageBucket": "scholarmind-99228.firebasestorage.app",
    "messagingSenderId": "51855942423",
    "appId": "1:51855942423:web:7594c01d745e0617a14d52",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)