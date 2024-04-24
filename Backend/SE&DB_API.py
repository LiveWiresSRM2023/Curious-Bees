from flask import Flask, request, jsonify
import requests
import qdrant_client
from qdrant_client.http import models
import numpy as np
from password import api_key,url

# setting up the DB
client = qdrant_client.QdrantClient(url=url,api_key=api_key)
collection_config = models.VectorParams(size=384,distance=models.Distance.COSINE)

# assign Qdrant Collection name
QdrantCollName = "testcollections"

app = Flask(__name__)

def model():
    # Placeholder for quantised mode;
    pass

def vectorize_content(id,content):
    # will vectorised and return the vector, the id comes out unfazed 
    # appropriate model and tokenizer should be used
    return id,embedding


def similarity(id,content):
    # the content is embedded and the id is pinned with it and sends as a dict
    id,embedding = vectorize_content(id,content)
    search = client.search(collection_name=QdrantCollName,search_params=models.SearchParams(hnsw_ef=128, exact=False),query_vector=embedding,limit=3)
    data = {point.id: point.score for point in search}
    return data

def send_db(id, data):
    # this vectorises the content and sends it to the db
    id,vector = vectorize_content(id,data)
    collection_config = models.VectorParams(size=384,distance=models.Distance.COSINE)
    if client.collection_exists(collection_name=QdrantCollName,vectors_config=collection_config):
        client.upsert(collection_name = QdrantCollName,points = models.Batch(id = id,vectors = vector))
  
def send_usr(data):
    return jsonify(data)
    # This function will send back json

def crossroads(data):
    # will decide what functions to do next based on th content  
    if data['type'] == 'post':
        send_db(data['id'], data['content'])
    elif data['type'] == 'search':
        send_usr(similarity(data['id'], data['content']))

@app.route('/', methods=['POST'])
def process_data():
    if requests.method == 'POST':
        data = request.json
        if 'user_id' in data and 'type' in data and 'content' in data and 'id_token' in data:
            try:
                # Verify Firebase ID token , still in prototype 
                decoded_token = auth.verify_id_token(data['id_token'])
                # Check if the user's ID is among the predefined keys
                if decoded_token['user_id'] in predefined_keys:
                    crossroads(data)
                    return jsonify({'message': 'Data processed successfully'})
                else:
                    return jsonify({'error': 'Unauthorized access'})
            except auth.InvalidIdTokenError:
                return jsonify({'error': 'Invalid ID token'})
            except auth.ExpiredIdTokenError:
                return jsonify({'error': 'Expired ID token'})
            except auth.RevokedIdTokenError:
                return jsonify({'error': 'Revoked ID token'})
            except auth.UserNotFoundError:
                return jsonify({'error': 'User not found'})
            except Exception as e:
                return jsonify({'error': str(e)})
        else:
            return jsonify({'error': 'Missing required fields'})
    else:
        return jsonify({'error': 'Method not allowed'})
    
if __name__ == '__main__':
    app.run(debug=True)