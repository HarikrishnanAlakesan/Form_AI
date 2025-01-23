import firebase_admin
from firebase_admin import credentials, firestore

# Check if Firebase has been initialized before initializing it again
if not firebase_admin._apps:
    try:
        # Initialize Firebase only if it hasn't been initialized already
        cred = credentials.Certificate(r'C:\Users\mailh\OneDrive\Desktop\New folder (2)\firebase-key.json')
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully.")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        exit(1)

# Get Firestore client
db = firestore.client()

def get_form_data():
    try:
        # Get all documents from the 'forms' collection
        forms_ref = db.collection('forms')
        docs = forms_ref.stream()

        # Print out all form submissions
        for doc in docs:
            print(f'Document ID: {doc.id}')
            print(f'Data: {doc.to_dict()}')

    except Exception as e:
        print(f"Error fetching form data: {e}")

# Fetch the stored form data
get_form_data()
