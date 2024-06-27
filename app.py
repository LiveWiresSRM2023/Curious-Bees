from flask import Flask, request, jsonify
import qdrant_client
from qdrant_client.http import models
from password import api_key,url
from llama_cpp import Llama 
import firebase_admin
from firebase_admin import credentials,firestore
import nltk
from rake_nltk import Rake
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import uuid 
import os

# setup firebase
# Check if the firebase app is already initialized or not
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceKey.json")
    app = firebase_admin.initialize_app(cred)

# setting up the DB
client = qdrant_client.QdrantClient(url=url,api_key=api_key)
collection_config = models.VectorParams(size=384,distance=models.Distance.DOT)

# assign Qdrant Collection name
QdrantCollName = "testcollections"

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

app = Flask(__name__)

def vectorize_content(id,content):
    model_path = "bge-small-en-v1.5-q4_k_m.gguf"
    model = Llama(model_path, embedding=True)
    embedding = model.embed(content)
    # will vectorised and return the vector, the id comes out 
    print(embedding)
    return id, embedding

def similarity(payload):
    # the content is embedded and searched in db which is then sent for similarity
    # and the top n results are returned with score and id as key value pair
    id, embedding = vectorize_content(payload["payload"], payload["content"])
    search = client.search(collection_name=QdrantCollName,search_params=models.SearchParams(hnsw_ef=128, exact=False),query_vector=embedding[0],limit=3)
    data = {point.id: point.score for point in search}
    return data

def send_db(payload):
    # this vectorises the content and sends it to the db with the same id as it was provided
    id,vector = vectorize_content(payload["id"], payload["content"])
    if not client.collection_exists(collection_name=QdrantCollName):
      client.create_collection(collection_name=QdrantCollName,vectors_config=collection_config)
    print(type(id))
    print(type(payload))
    print(type(vector))
    client.upsert(collection_name=QdrantCollName, points=[
        models.PointStruct(
            id = id,
            vector = vector,
            payload= payload
        )])
  
def send_usr(data):
    return jsonify(data)
    # This function will send back json

def authenticate(uid:str):
    db = firestore.client()
    query = db.collection(u'users').where(u'uid', u'==', uid).get()
    result = [x.to_dict() for x in query] # Get user with the specific

    if result == []:
        return False
    else:
        return True

def crossroads(data):
    # will decide what functions to do next based on th content  
    if data['type'] == 'post':
        send_db(data)
    elif data['type'] == 'search':
        send_usr(similarity(data))

#Function for finding keywords using RAKE 
def get_keywords(text):
    nltk.download('punkt')
    nltk.download('stopwords')
    rake = Rake() 
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases()
    return keywords


# Signing into the user's mail id
def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            flow.redirect_uri = 'http://localhost:8080/'  # Fixed redirect URI
            creds = flow.run_local_server(port=8080)  # Fixed port
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

@app.route('/')
def home():
    return jsonify({
        "Flask API" : "Running"
    })

@app.route('/post', methods=['POST'])
def process_data():
    if request.method == 'POST':
        data = request.json
        if 'user_id' in data and 'type' in data and 'content' in data and 'id' in data:
            try:
                if authenticate(data['user_id']) == True:
                    crossroads(data)
                    return jsonify({'msg': 'Data processed successfully'})
                else:
                    return jsonify({'msg': 'Unauthorized access'})
            except Exception as e:
                print(e)
                return jsonify({'msg': 'There was an error'})
        else:
            return jsonify({'error': 'Missing required fields'})
    else:
        return jsonify({'error': 'Method not allowed'})

@app.route('/keywords', methods=['POST'])
def extract_keywords():
    if request.method == 'POST':
        data = request.json
        if 'content' in data:
            try:
                if authenticate(data['user_id']) == True:
                    content = data['content']
                    keywords = get_keywords(content)
                    return jsonify({"keywords": keywords})
                else:
                    return jsonify({'msg': 'Unauthorized access'})
            except Exception as e:
                print(e)
                return jsonify({'msg': 'There was an error'})
        else:
            return jsonify({'error': 'Missing content field'})
    else:
        return jsonify({'error': 'Method not allowed'})

@app.route('/create_event', methods=['POST'])
def create_event():
    if request.method == 'POST':
        data = request.json
        if 'user_id' in data and 'summary' in data and 'description' in data and 'start_time' in data and 'end_time' in data and 'attendees' in data:
            try:
                if authenticate(data['user_id']) == True:
                    summary = data['summary']
                    description = data['description']
                    start_time = data['start_time']
                    end_time = data['end_time']
                    attendees_emails = data['attendees']

                    creds = get_credentials()
                    service = build('calendar', 'v3', credentials=creds)

                    attendees = [{'email': email} for email in attendees_emails]

                    event = {
                        'summary': summary,
                        'description': description,
                        'start': {
                            'dateTime': start_time,
                            'timeZone': 'America/Los_Angeles',
                        },
                        'end': {
                            'dateTime': end_time,
                            'timeZone': 'America/Los_Angeles',
                        },
                        'attendees': attendees,
                        'conferenceData': {
                            'createRequest': {
                                'requestId': str(uuid.uuid4()),  # Any unique string
                                'conferenceSolutionKey': {
                                    'type': 'hangoutsMeet'
                                }
                            }
                        },
                    }

                    created_event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
                    return jsonify({'msg': 'Event created successfully', 'link': created_event.get("htmlLink")})

                else:
                    return jsonify({'msg': 'Unauthorized access'}), 401
            except Exception as e:
                print(e)
                return jsonify({'msg': 'There was an error', 'error': str(e)}), 500
        else:
            return jsonify({'error': 'Missing required fields'}), 400
    else:
        return jsonify({'error': 'Method not allowed'}), 405


if __name__ == '__main__':
    app.run(debug=True, port=5000)
