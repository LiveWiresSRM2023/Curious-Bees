import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import uuid
import json

# Initialize Firebase
cred = credentials.Certificate("serviceKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def read_posts_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def create_post(post_data):
    post_data["timestamp"] = datetime.datetime.now().isoformat()  # Adds current timestamp
    return post_data

def main():
    # THE INPUT IS READ FROM A JSON FILE
    posts = read_posts_from_file("input.json")

    for post_data in posts:
        post = create_post(post_data)
        
        doc_id = str(uuid.uuid4())

        doc_ref = db.collection("posts").document(doc_id)
        doc_ref.set(post)
        print(f"Post created successfully with ID: {doc_id}")

if __name__ == "__main__":
    main()
