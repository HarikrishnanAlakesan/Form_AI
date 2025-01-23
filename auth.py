import requests

# Firebase Web API Key (found in Project Settings > General > Web API Key)
API_KEY = "AIzaSyCY9b5I9T13Mps6agdwpbqOHpWHEwNxENs"

# Function to register a new user
def register_user(email, password):
    try:
        from firebase_admin import auth
        user = auth.create_user(email=email, password=password)
        return {"success": True, "uid": user.uid}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Function to log in a user
def login_user(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return {"success": True, "data": response.json()}
    else:
        return {"success": False, "error": response.json()}
