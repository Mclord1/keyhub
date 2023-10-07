from dotenv import load_dotenv

load_dotenv()

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='mclord@velrusglobal.com',
    to_emails='clairclancy@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    print(os.environ.get('SENDGRID_API_KEY'))
    sg = SendGridAPIClient('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')
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)