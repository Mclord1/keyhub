import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='mclordemuraishe@gmail.com',
    to_emails='mclordemuraishe@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient("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")
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)