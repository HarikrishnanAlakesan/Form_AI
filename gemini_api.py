import google.generativeai as genai

# Configure Gemini API with your API Key
api_key = "AIzaSyAuDGrMaNQZxj-IDml8iWXNYQXsrq7DGf8"
genai.configure(api_key=api_key)

# Create the model with specific parameters
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
        "The user will provide details about the type of form they need (such as a contact form, survey form, etc.) "
        "and the fields they want in the form.\n\nUser Input: {User's form type, e.g., 'Contact Form'} "
        "and {fields the user wants in the form, e.g., 'Name, Email, Message'}\n\nPlease generate the corresponding "
        "HTML form code that includes:\n1. An appropriate form tag with method='POST'.\n2. Text input fields for text-based "
        "inputs like 'Name' and 'Email'.\n3. A textarea field for longer inputs like 'Message'.\n4. A submit button.\n5. "
        "Any necessary labels, placeholders, and field types.\n6. Ensure that the form is user-friendly and visually organized."
    ),
)

# Start the chat session with predefined user input (you can adjust as needed)
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": ["I want a job application form with the following fields: Name, Email, Phone Number, Resume (file upload), and a Submit button."]
        }
    ]
)

# Sending message from user to generate form
response = chat_session.send_message("Generate the job application form as per the user input")

# Extracting and printing the generated HTML form code
print(response.text)
