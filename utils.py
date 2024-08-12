from firebase_admin import firestore
import nltk
from rake_nltk import Rake
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
from qdrant_utils import send_db , delete_vector

# Qdrant collection name
QdrantCollName = "testcollections"

def authenticate(uid: str):
    """
    Authenticates the user by checking if their UID exists in the Firestore database.
    """
    db = firestore.client()
    query = db.collection(u'users').where(u'uid', u'==', uid).get()
    result = [x.to_dict() for x in query]

    if result == []:
        return False
    else:
        return True

def posthandler(data):
    """
    Routes the request to the appropriate function based on the 'type' in the request data.
    Handles both posting data and deleting vectors.
    """
    if data['type'] == 'post':
        send_db(data)
        return {"status": "Data stored successfully"}
    elif data['type'] == 'delete':
        return delete_vector(data['id'])
    else:
        return {"error": "Invalid type provided"}

def get_keywords(text):
    """
    Extracts keywords from the provided text using the RAKE algorithm.
    """
    nltk.download('punkt')
    nltk.download('stopwords')
    rake = Rake()
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases()
    return keywords

def get_credentials():
    """
    Authenticates and returns Google Calendar API credentials.
    If the credentials are expired or not present, the user is prompted to log in.
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            flow.redirect_uri = 'http://localhost:8080/'
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
