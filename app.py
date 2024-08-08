from flask import Flask, request, jsonify
import qdrant_client
from qdrant_client.http import models
from llama_cpp import Llama 
import firebase_admin
from firebase_admin import credentials, firestore
import nltk
from rake_nltk import Rake
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import uuid 
import os

# Initialize Firebase Admin SDK with the service account key if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceKey.json")
    app = firebase_admin.initialize_app(cred)

# Set up the Qdrant client and collection configuration
client = qdrant_client.QdrantClient(url="localhost:6333")
collection_config = models.VectorParams(size=384, distance=models.Distance.DOT)

# Qdrant collection name
QdrantCollName = "testcollections"

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

app = Flask(__name__)

def vectorize_content(id, content):
    """
    Vectorizes the provided content using the Llama model and returns the vector and ID.
    """
    model_path = "bge-small-en-v1.5-q4_k_m.gguf"
    model = Llama(model_path, embedding=True)
    embedding = model.embed(content)
    print(embedding)
    return id, embedding

def similarity(payload):
    """
    Searches the Qdrant database for similar content based on the vectorized input and returns the top results.
    """
    id, embedding = vectorize_content(payload["payload"], payload["content"])
    search = client.search(
        collection_name=QdrantCollName,
        search_params=models.SearchParams(hnsw_ef=128, exact=False),
        query_vector=embedding[0],
        limit=3
    )
    data = {point.id: point.score for point in search}
    return data

def send_db(payload):
    """
    Vectorizes the content and sends it to the Qdrant database with the provided ID.
    """
    id, vector = vectorize_content(payload["id"], payload["content"])
    if not client.collection_exists(collection_name=QdrantCollName):
        client.create_collection(collection_name=QdrantCollName, vectors_config=collection_config)
    client.upsert(
        collection_name=QdrantCollName, 
        points=[models.PointStruct(id=id, vector=vector, payload=payload)]
    )

def send_usr(data):
    """
    Sends back a JSON response to the user.
    """
    return jsonify(data)

def authenticate(uid: str):
    """
    Authenticates the user by checking if their UID exists in the Firestore database.
    """
    db = firestore.client()
    query = db.collection(u'users').where(u'uid', u'==', uid).get()
    result = [x.to_dict() for x in query]  # Get user with the specific UID

    return bool(result)

def crossroads(data):
    """
    Routes the request to the appropriate function based on the 'type' in the request data.
    """
    if data['type'] == 'post':
        send_db(data)
    elif data['type'] == 'search':
        send_usr(similarity(data))

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
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            flow.redirect_uri = 'http://localhost:8080/'  # Fixed redirect URI
            creds = flow.run_local_server(port=8080)  # Fixed port
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

@app.route('/')
def home():
    """
    A simple home route to check if the Flask API is running.
    """
    return jsonify({"Flask API": "Running"})

@app.route('/post', methods=['POST'])
def process_data():
    """
    Processes incoming data for either storage or similarity search based on the request type.
    Authentication is required.
    """
    if request.method == 'POST':
        data = request.json
        if 'user_id' in data and 'type' in data and 'content' in data and 'id' in data:
            try:
                if authenticate(data['user_id']):
                    crossroads(data)
                    return jsonify({'msg': 'Data processed successfully'})
                else:
                    return jsonify({'msg': 'Unauthorized access'}), 401
            except Exception as e:
                print(e)
                return jsonify({'msg': 'There was an error', 'error': str(e)}), 500
        else:
            return jsonify({'error': 'Missing required fields'}), 400
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/keywords', methods=['POST'])
def extract_keywords():
    """
    Extracts keywords from the provided content using RAKE.
    Authentication is required.
    """
    if request.method == 'POST':
        data = request.json
        if 'content' in data:
            try:
                if authenticate(data['user_id']):
                    content = data['content']
                    keywords = get_keywords(content)
                    return jsonify({"keywords": keywords})
                else:
                    return jsonify({'msg': 'Unauthorized access'}), 401
            except Exception as e:
                print(e)
                return jsonify({'msg': 'There was an error', 'error': str(e)}), 500
        else:
            return jsonify({'error': 'Missing content field'}), 400
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/create_event', methods=['POST'])
def create_event():
    """
    Creates a Google Calendar event with the provided details.
    Authentication is required.
    """
    if request.method == 'POST':
        data = request.json
        if 'user_id' in data and 'summary' in data and 'description' in data and 'start_time' in data and 'end_time' in data and 'attendees' in data:
            try:
                if authenticate(data['user_id']):
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
