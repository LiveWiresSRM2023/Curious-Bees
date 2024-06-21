# Flask SendGrid Email Sending Service

This Flask application provides an endpoint to send emails using the SendGrid API.

## Prerequisites

1. **Sign up for a SendGrid account**:

   - Sign up for a free SendGrid account [here](https://signup.sendgrid.com/).

2. **Enable Two-factor authentication**:

   - Follow the instructions [here](https://sendgrid.com/docs/ui/account-and-settings/two-factor-authentication/) to enable 2FA.

3. **Create and store a SendGrid API Key**:

   - Visit the API Key documentation [here](https://sendgrid.com/docs/ui/account-and-settings/api-keys/) to create an API key with `Mail Send > Full Access` permissions.
   - Store this API key in an environment variable, e.g., `SENDGRID_API_KEY`.

4. **Complete Domain Authentication**:
   - Follow the instructions [here](https://sendgrid.com/docs/ui/account-and-settings/how-to-set-up-domain-authentication/) to verify your sender identity.

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **create a virtual env**:

   ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS and Linux
    .\venv\Scripts\activate   # On Windows
   ```

3. **Dependencies installations**:

   pip install -r requirements.txt

4. **create an .env file**

   touch .env

5. **Add your environment variables to ".env"**:

   SENDGRID_API_KEY=your_sendgrid_api_key
   REGISTERED_EMAIL=your_verified_sender_email

## Usage

1. **Run the flask app**:

   python app.py

2. **Test the App**:
   You can use a tool like curl or Postman to send a POST request to http://127.0.0.1:5000/send-email with the following JSON payload:

   code--

   {
   "to_email": "recipient@example.com",
   "subject": "Personalized Email Subject",
   "content": "Hello, this is a personalized email content!"
   }

**Example for CURL COMMAND**:

curl -X POST http://127.0.0.1:5000/send-email -H "Content-Type: application/json" -d '{
"to_email": "recipient@example.com",
"subject": "Personalized Email Subject",
"content": "Hello, this is a personalized email content!"
}'
