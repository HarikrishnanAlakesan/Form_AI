import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    try:
        # Check if Firebase has already been initialized
        if not firebase_admin._apps:
            # Initialize Firebase if it hasn't been initialized
            cred = credentials.Certificate(r'C:\Users\mailh\OneDrive\Desktop\New folder (2)\firebase_config.json')
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully.")
        else:
            print("Firebase already initialized.")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")

# Call the function to initialize Firebase
initialize_firebase()
