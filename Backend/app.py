from flask import Flask, request, jsonify
import qdrant_client
from qdrant_client.http import models
from qdrant_client.models import Distance, VectorParams
from password import api_key, url
from llama_cpp import Llama
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from waitress import serve

# setup firebase
# Check if the firebase app is already initialized or not
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceKey.json")
    app = firebase_admin.initialize_app(cred)

# setting up the DB
client = qdrant_client.QdrantClient(url=url, api_key=api_key)
collection_config = models.VectorParams(size=384, distance=models.Distance.DOT)

# assign Qdrant Collection name
QdrantCollName = "testcollections"

app = Flask(__name__)

def vectorize_content(id, content):
    model_path = "bge-small-en-v1.5-q4_k_m.gguf"
    model = Llama(model_path, embedding=True)
    embedding = model.embed(content)
    # will vectorise and return the vector, the id comes out 
    print(embedding)
    return id, embedding

def similarity(payload):
    # the content is embedded and searched in db which is then sent for similarity
    # and the top n results are returned with score and id as key value pair
    id, embedding = vectorize_content(payload["payload"], payload["content"])
    search = client.search(collection_name=QdrantCollName, search_params=models.SearchParams(hnsw_ef=128, exact=False), query_vector=embedding[0], limit=3)
    data = {point.id: point.score for point in search}
    return data

def send_db(payload):
    # this vectorises the content and sends it to the db with the same id as it was provided
    id, vector = vectorize_content(payload["id"], payload["content"])
    if not client.collection_exists(collection_name=QdrantCollName):
        client.create_collection(collection_name=QdrantCollName, vectors_config=collection_config)
    print(type(id))
    print(type(payload))
    print(type(vector))
    client.upsert(collection_name=QdrantCollName, points=[
        models.PointStruct(
            id=id,
            vector=vector,
            payload=payload
        )])

def send_usr(data):
    return jsonify(data)
    # This function will send back json

def authenticate(uid: str):
    db = firestore.client()
    query = db.collection(u'users').where(u'uid', u'==', uid).get()
    result = [x.to_dict() for x in query]  # Get user with the specific

    if result == []:
        return False
    else:
        return True

def crossroads(data):
    # will decide what functions to do next based on the content  
    if data['type'] == 'post':
        send_db(data)
    elif data['type'] == 'search':
        send_usr(similarity(data))

@app.route('/')
def home():
    return jsonify({
        "Flask API": "Running"
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

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)
