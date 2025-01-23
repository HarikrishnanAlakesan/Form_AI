import os
from flask import Flask, request, jsonify, render_template_string, redirect, url_for, flash, session
import google.generativeai as genai
from firebase_config import initialize_firebase
from auth import register_user, login_user

# Initialize Firebase
initialize_firebase()

# Configure Gemini API with your API Key
api_key = "AIzaSyAuDGrMaNQZxj-IDml8iWXNYQXsrq7DGf8"
genai.configure(api_key=api_key)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure session key for flash messages and redirects

# Function to generate HTML form from Gemini API
def generate_form_from_gemini(form_type, fields):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction=(
            "Create an HTML form based on the following user input. "
            "The user will provide details about the type of form they need (such as a student form, job application form, etc.) "
            "and the fields they want in the form.\n\nUser Input: {User's form type, e.g., 'Student Form'} "
            "and {fields the user wants in the form, e.g., 'Name, Email, Age, Grade'}\n\nPlease generate the corresponding "
            "HTML form code that includes:\n1. An appropriate form tag with method='POST'.\n2. Text input fields for text-based "
            "inputs like 'Name' and 'Email'.\n3. A submit button.\n4. Any necessary labels, placeholders, and field types.\n"
            "5. Ensure that the form is user-friendly and visually organized."
        ),
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [f"I want a {form_type} with the following fields: {', '.join(fields)}"]
            }
        ]
    )

    response = chat_session.send_message(f"Generate the {form_type} form as per the user input")
    return response.text

# Login Route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Authenticate the user with Firebase
        result = login_user(email, password)
        
        if result['success']:
            # Store user email in session after successful login
            session['user'] = email
            return redirect(url_for('form_generator'))  # Redirect to form generation page
        else:
            flash(f"Login failed: {result['error']}", 'danger')
            return redirect(url_for('login'))
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: #fff;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .login-container {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px 30px;
            width: 300px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            text-align: center;
        }

        .login-container h2 {
            margin-bottom: 20px;
        }

        .login-container label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }

        .login-container input {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: none;
            border-radius: 5px;
        }

        .login-container input:focus {
            outline: none;
            box-shadow: 0 0 5px #fff;
        }

        .login-container button {
            background-color: #4caf50;
            color: white;
            border: none;
            padding: 10px 15px;
            width: 100%;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }

        .login-container button:hover {
            background-color: #45a049;
        }

        .login-container p {
            margin-top: 15px;
        }

        .login-container a {
            color: #4caf50;
            text-decoration: none;
            font-weight: bold;
        }

        .login-container a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Login</h2>
        <form method="POST">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" placeholder="Enter your email" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>
            <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <a href="/register">Register</a></p>
    </div>
</body>
</html>

    """)

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = register_user(email, password)
        
        if result['success']:
            flash("Registration successful!", 'success')
            return redirect(url_for('login'))  # Redirect to login page after registration
        else:
            flash(f"Registration failed: {result['error']}", 'danger')
    
    return render_template_string("""
        <h2>Register</h2>
        <form method="POST">
            <label for="email">Email:</label>
            <input type="email" name="email" required><br>
            <label for="password">Password:</label>
            <input type="password" name="password" required><br>
            <button type="submit">Register</button>
        </form>
    """)

# Form Generation Page
@app.route('/form_generator')
def form_generator():
    if 'user' not in session:
        return redirect(url_for('login'))  # If not logged in, redirect to login page
    
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: #fff;
            margin: 0;
            padding: 20px;
        }

        h1 {
            text-align: center;
            margin-bottom: 20px;
        }

        p {
            text-align: center;
            margin-bottom: 30px;
            font-size: 16px;
        }

        label {
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: none;
            border-radius: 5px;
        }

        input[type="text"]:focus {
            outline: none;
            box-shadow: 0 0 5px #fff;
        }

        button {
            background-color: #4caf50;
            color: white;
            border: none;
            padding: 10px 15px;
            width: 100%;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

        #generatedFormContainer {
            margin-top: 30px;
            background-color: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }
    </style>
</head>
<body>
    <h1>Dynamic Form Generator</h1>
    <p>Fill in the details below and click "Generate Form" to create a custom form:</p>

    <!-- Input Fields for Form Type and Fields -->
    <label for="formType">Form Type (e.g., Student Form):</label>
    <input type="text" id="formType" placeholder="Enter form type" />

    <label for="fields">Fields (comma separated, e.g., Name, Email, Age, Grade):</label>
    <input type="text" id="fields" placeholder="Enter form fields" />

    <button onclick="generateForm()">Generate Form</button>

    <!-- Display Generated Form -->
    <div id="generatedFormContainer"></div>

    <script>
        async function generateForm() {
            // Get the form type and fields from the input
            const formType = document.getElementById('formType').value.trim();
            const fields = document.getElementById('fields').value.trim().split(',');

            // Validate input
            if (!formType || fields.length === 0) {
                alert('Please provide both form type and fields.');
                return;
            }

            // Send input to the backend via a POST request
            const response = await fetch('/generate_form', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ formType, fields })
            });

            // Parse and display the generated form
            const data = await response.json();
            if (data.form) {
                document.getElementById('generatedFormContainer').innerHTML = data.form;
            } else {
                alert('Error generating form.');
            }
        }
    </script>
</body>
</html>

    """)

# Route to generate form
@app.route('/generate_form', methods=['POST'])
def generate_form():
    data = request.get_json()
    form_type = data.get('formType')
    fields = data.get('fields')
    if not form_type or not fields:
        return jsonify({"error": "Form type and fields are required"}), 400

    # Generate the HTML form from Gemini
    form_html = generate_form_from_gemini(form_type, fields)

    # Return the generated form as a JSON response
    return jsonify({"form": form_html})

# Route to handle form submissions
@app.route('/submit_admission', methods=['POST'])
def submit_admission():
    data = request.json  # For JSON payload
    print("Form Data Received:", data)  # Print form data to terminal
    return jsonify({'message': 'Admission submitted successfully', 'data': data})

if __name__ == '__main__':
    app.run(debug=True)
