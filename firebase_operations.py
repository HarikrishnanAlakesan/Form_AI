import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase using the service account key file (firebase_key.json)
cred = credentials.Certificate(r'C:\Users\mailh\OneDrive\Desktop\New folder (2)\firebase-key.json')  # Provide path to firebase_key.json
firebase_admin.initialize_app(cred)

# Reference to Firestore
db = firestore.client()

# Function to save form data
def save_form_data(form_data):
    try:
        # Reference to the "forms" collection
        forms_ref = db.collection('forms')

        # Add a new document with the form data
        forms_ref.add(form_data)
        print("Form data saved successfully.")
    except Exception as e:
        print(f"Error saving form data: {e}")

# Example form data
form_data = {
    'formType': 'Student Form',
    'fields': ['Name', 'Email', 'Age', 'Grade'],
    'userEmail': 'user@example.com',
}

save_form_data(form_data)
