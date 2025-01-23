from flask import Flask, request, render_template
from firebase_config import initialize_firebase
from auth import register_user, login_user

# Initialize Firebase
initialize_firebase()

# Initialize Flask App
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = login_user(email, password)
        if result['success']:
            return f"Welcome, {email}!"
        else:
            return f"Login failed: {result['error']}"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = register_user(email, password)
        if result['success']:
            return "Registration successful!"
        else:
            return f"Registration failed: {result['error']}"
    return '''
    <h2>Register</h2>
    <form method="POST">
        <label for="email">Email:</label>
        <input type="email" name="email" required><br>
        <label for="password">Password:</label>
        <input type="password" name="password" required><br>
        <button type="submit">Register</button>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
