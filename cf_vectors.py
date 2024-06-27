from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceKey.json")
    app = firebase_admin.initialize_app(cred)

firestore_client = firestore.client()

collection = firestore_client.collection("coffee-beans")
doc = {
  "name": "Kahawa coffee beans",
  "description": "Information about the Kahawa coffee beans.",
  "embedding_field": Vector([1.0 , 2.0, 3.0])
}

collection.add(doc)
    