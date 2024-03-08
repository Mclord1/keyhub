from dotenv import load_dotenv
import base64
from pathlib import Path
import os
import mailtrap as mt

load_dotenv()

token = "f45fb90ea2ca196d3e67ae7c4ef78389"
base_url = "http://3.145.101.11:5000/"


class EmailHandler:

    @classmethod
    def welcome_mail(cls, recipient, username):
        subject = '<h2 class="bold">Your Keyhub Account has been created.</h2>'
        body = """

                <p>
                    Now that your account has been created, click the button below to setup your password so that you
                    can login to your account. After that, you can always log into your account using your email address
                    and the password you have set up!
                </p>

                <!-- Add your reset password link -->
                <a href="#" class="mb-20">Reset Password</a>

        """

        return cls.send_email(recipient, subject, username, body)

    @classmethod
    def send_otp(cls, recipient, otp):
        subject = '<h2 class="bold">Your Keyhub Account OTP</h2>'
        body = f"""

                <p>
                   Your OTP is <b>{otp}.</b> The OTP expires in 2 minutes.</p>
                </p>

                <!-- Add your reset password link -->
                <a href="#" class="mb-20">Reset Password</a>

        """

        return cls.send_email(recipient, subject, recipient, body)

    @classmethod
    def send_email(cls, recipient, subject, username, body):
        mail = mt.Mail(
            sender=mt.Address(email="mailtrap@axetechinnovations.com", name="Keyhub"),
            to=[mt.Address(email=recipient, name="clair")],
            subject=subject,
            html=f"""
            <!doctype html>
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Account Created</title>
                <style>
                    @font-face {{
                        font-family: 'QuickSand';
                        src: url('{base_url}fonts/quicksand/Quicksand-Regular.ttf') format('woff2'),
                        url('{base_url}fonts/quicksand/Quicksand-Regular.ttf') format('woff');
                    }}
    
                    @font-face {{
                        font-family: 'QuickSand Bold';
                        src: url('{base_url}fonts/quicksand/Quicksand-Bold.ttf') format('woff2'),
                        url('{base_url}fonts/quicksand/Quicksand-Bold.ttf') format('woff');
                    }}
    
                    body {{
                        margin: 0;
                        padding: 0;
                        font-family: 'QuickSand', sans-serif;
                        background-color: #fff;
                    }}
    
                    .container {{
                        max-width: 50%;
                        margin: auto;
                    }}
    
                    .header-container {{
                        height: 400px; /* Adjust the height as needed */
                        background-image: url('{base_url}images/login_image.png');
                        background-size: contain;
                        background-position: center;
                    }}
    
                    .bold {{
                        font-family: 'QuickSand Bold', 'Arial', sans-serif;
                    }}
    
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                    }}
    
                    img {{
                        width: 100%;
                        height: auto;
                    }}
    
                    td {{
                        padding: 20px;
                        text-align: left;
                    }}
    
                    h2 {{
                        color: #333;
                        font-size: 35px;
                    }}
    
                    a {{
                        display: inline-block;
                        padding: 20px 30px;
                        background-color: #007BFF;
                        color: #fff;
                        text-decoration: none;
                        border-radius: 5px;
                    }}
    
                    p {{
                        color: #555;
                        line-height: 30px;
                        margin: 0 0 20px 0;
                    }}
    
                    footer {{
                        background-color: #F5F6FA;
                        padding: 10px;
                        text-align: center;
                    }}
    
                    footer > img {{
                        height: 50px;
                        width: auto;
                    }}
    
                    footer > p {{
                        margin: 0;
                    }}
    
                    .mb-20 {{
                        margin-bottom: 20px !important;
                    }}
                </style>
            </head>
            <body>
            <div class="container">
                <!-- Header with Full-width Image -->
                <div class="header-container"></div>
    
                <!-- Email Content -->
                <table>
                    <tr>
                        <td>
                            <h2 class="bold">{subject}</h2>
    
                            <p>Hello <span class="bold">{username}</span>,</p>
                            
                            {body}
    
                            <p>
                                Best Regards, <br>The Keyhub Academy Team
                            </p>
    
                        </td>
                    </tr>
                </table>
    
                <!-- Footer -->
                <footer>
                    <p>&copy; KeyHub, <span id="currentYear"></span>. All Rights Reserved</p>
                    <p>123 Main St, City</p>
                    <p class="mb-20">Lagos, Nigeria</p>
                    <img src="{base_url}images/old_logo.png" alt="Logo">
                </footer>
            </div>
    
            <!-- JavaScript to get and display the current year -->
            <script>
                document.getElementById('currentYear').innerHTML = new Date().getFullYear();
            </script>
            </body>
            </html>
    
            """
        )

        client = mt.MailtrapClient(token=token)
        client.send(mail)
        return True
