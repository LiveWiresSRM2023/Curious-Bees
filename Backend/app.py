from flask import Flask, request, jsonify
import requests
import qdrant_client
from qdrant_client.http import models
from password import api_key,url
from llama_cpp import Llama
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# setup firebase
# Check if the firebase app is already initialized or not
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceKey.json")
    app = firebase_admin.initialize_app(cred)

# setting up the DB
client = qdrant_client.QdrantClient(url=url,api_key=api_key)
collection_config = models.VectorParams(size=384,distance=models.Distance.COSINE)

# assign Qdrant Collection name
QdrantCollName = "testcollections"

app = Flask(__name__)


def vectorize_content(id,content):
    model_path = "bge-small-en-1.5-Q_4_K_M.gguf"
    model = Llama(model_path, embedding=True)
    embedding = model.embed(content)
    # will vectorised and return the vector, the id comes out unfazed, 
    print(embedding)
    return id,embedding

def similarity(id,content):
    # the content is embedded and the id is pinned with it and sends as a dict
    id,embedding = vectorize_content(id,content)
    print(embedding)
    search = client.search(collection_name=QdrantCollName,search_params=models.SearchParams(hnsw_ef=128, exact=False),query_vector=embedding[0],limit=3)
    data = {point.id: point.score for point in search}
    return data

def send_db(id, data):
    # this vectorises the content and sends it to the db
    id,vector = vectorize_content(id,data)
    collection_config = models.VectorParams(size=384,distance=models.Distance.COSINE)
    if client.collection_exists(collection_name=QdrantCollName, vectors_config=collection_config):
        client.upsert(collection_name = QdrantCollName,points = models.Batch(id =[id],vectors = vector))
  
def send_usr(data):
    return jsonify(data)
    # This function will send back json

def authenticate(uid:str):
    db = firestore.client()
    query = db.collection(u'users').where(u'uid', u'==', uid).get()
    result = [x.to_dict() for x in query] # Get user with the specific
    print(result)
    if result == []:
        return False
    else:
        return True

def crossroads(data):
    # will decide what functions to do next based on th content  
    if data['type'] == 'post':
        send_db(data['id'], data['content'])
    elif data['type'] == 'search':
        send_usr(similarity(data['id'], data['content']))

@app.route('/', methods=['POST'])
def process_data():
    if request.method == 'POST':
        data = request.json
        if 'user_id' in data and 'type' in data and 'content' in data and 'id_token' in data:
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
    
if __name__ == '__main__':
    app.run(debug=True, port=8000)