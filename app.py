from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from utils import authenticate, posthandler, get_keywords, get_credentials
from qdrant_utils import  similarity
from googleapiclient.discovery import build
import firebase_admin
from firebase_admin import credentials

# Initialize Firebase Admin SDK with the service account key if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceKey.json")
    firebase_admin.initialize_app(cred)

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

@app.route('/')
def home():
    """
    A simple home route to check if the Flask API is running.
    """
    return jsonify({"Flask API": "Running"})

@app.route('/posthandler', methods=['POST'])
def process_data():
    """
    Processes incoming data for either storage or deletion based on the request type.
    Authentication is required.
    """
    if request.method == 'POST':
        data = request.json
        if 'user_id' in data and 'type' in data:
            try:
                if True:
                    return jsonify(posthandler(data))
                else:
                    return jsonify({'msg': 'Unauthorized access'}), 401
            except Exception as e:
                return jsonify({'msg': 'There was an error', 'error': str(e)}), 500
        else:
            return jsonify({'error': 'Missing required fields'}), 400
    else:
        return jsonify({'error': 'Method not allowed'}), 405

@app.route('/search', methods=['POST'])
def search_data():
    """
    Handles the search functionality separately.
    Authentication is required.
    """
    if request.method == 'POST':
        data = request.json
        if 'user_id' in data and 'content' in data:
            try:
                if True:
                    return jsonify(similarity(data))
                else:
                    return jsonify({'msg': 'Unauthorized access'}), 401
            except Exception as e:
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
                if True:
                    content = data['content']
                    keywords = get_keywords(content)
                    return jsonify({"keywords": keywords})
                else:
                    return jsonify({'msg': 'Unauthorized access'}), 401
            except Exception as e:
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
                if True:
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
                                'requestId': str(uuid.uuid4()),
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
                return jsonify({'msg': 'There was an error', 'error': str(e)}), 500
        else:
            return jsonify({'error': 'Missing required fields'}), 400
    else:
        return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(debug=True, port=7000)
