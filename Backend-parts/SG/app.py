from flask import Flask, request, jsonify
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
# unable to get the api key ss the website was tripping 
load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>hellow flask</h1>"


@app.route("/send-email",methods = ['POST'])

def send_email():
    
    # data = request.get_json() oonce the testing is done cmt out this line for production purpose and remove the data dict below
    # for testing porpose
    data = {
    "to_email": "recipient@example.com", #reset with the testing email id for reciever
    "subject": "Personalized Email Subject",
    "content": "Hello, this is a personalized email content!"
}

    if not data or not "to_email" in data or not 'subject' in data or not 'content' in data:
        return jsonify({"error": "Missing required parameters"}) , 400
    
    sendgrid_api = os.getenv('API_SECRET_KEY') 
    if not sendgrid_api:
        return jsonify({'error':"Missing the required api key for sendng mails"}), 400
    
    from_email = os.getenv("REGISTERED_EMAIL")
    if not from_email:
        return jsonify({"error","Missing the required registered email with sendgrid account"}), 400
    

    to_email = data['to_email']
    subject = data['subject']
    content = data['content']


    message = Mail(
                    from_email= from_email,
                   to_emial = to_email,
                   subject= subject,
                   html_content= content
                   )

    try:
        send_grid = SendGridAPIClient(api_key=sendgrid_api)
        response = send_grid.send(message)

        return jsonify({
            "message":"Email sent successfully", 
            "status code": response.status_code
            }) , response.status_code
    except Exception as e:

        return jsonify({
            "error" : str(e)
        }) , 500
    


if __name__ == "__main__":
    app.run(debug=True)