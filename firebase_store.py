from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r'C:\Users\mailh\OneDrive\Desktop\New folder (2)\firebase-key.json')
firebase_admin.initialize_app(cred)

# Create Firestore client
db = firestore.client()

def store_form_data(form_data):
    # Specify the collection and document where you want to store the data
    # In this case, we'll store the form data under a new document in the 'forms' collection
    doc_ref = db.collection('forms').document()  # Automatically generates a unique document ID
    doc_ref.set(form_data)
    print("Data stored successfully!")

# Flask route to handle form submission
@app.route('/submit_admission', methods=['POST'])
def submit_form():
    # Get the submitted form data from the request
    form_data = request.json  # Assuming the form data is sent as JSON

    # Store the form data in Firestore
    store_form_data(form_data)

    # Return a success response
    return jsonify({'message': 'Form data submitted successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
