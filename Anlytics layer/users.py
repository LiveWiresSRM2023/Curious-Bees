import firebase_admin
from firebase_admin import credentials,firestore
from firebase_admin.firestore import SERVER_TIMESTAMP


initialize_firebase()
db = firestore.client()

def add_timestamp(collection_name):
    collection_ref = db.collection(collection_name)

    docs = collection_ref.stream()

    batch=db.batch()

    for doc in docs:
        doc_ref = collection_ref.document(doc.id)

        batch.update(doc_ref,{'timestamp':SERVER_TIMESTAMP})

        try:
            batch.commit()
            print(f"Updated document {doc.id} with timestamp.")
        except Exception as e:
            print('Error')
          
add_timestamp('users')
