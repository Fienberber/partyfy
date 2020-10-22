from flask_sqlalchemy import SQLAlchemy
from app import app
from app.user import User

import secrets
from app.smtp_setup import smtp_server, port, sender_email, password
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


db = SQLAlchemy(app)



def sendNewPassword(_email):
    new_password = secrets.token_urlsafe(16)

    user = User.query.filter_by(email=_email).first()
    if(user is None): return False

    sendEmail(new_password, _email)
    user.setPassword(new_password)
    return True


def sendEmail(content, receiver_email):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Partyfy ! New password"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = """\
        <html>
        <head>
        
        </head>
        <body style="color: #283845; font-family: 'Geneva', sans-serif; margin: 20px; background-image: linear-gradient(-225deg, #7DE2FC 0%, #B9B6E5 100%); background-repeat: no-repeat; background-attachment: fixed; background-size: cover;">
        <div class="center" style="text-align: center; float: center; margin: 0; position: absolute; top: 30%; left: 50%; -ms-transform: translateX(-50%); transform: translateX(-50%);">
            <h1 style="font-family: 'futura', 'helvetica', sans-serif; color: white; font-size: 30px;">
            Your new Partyfy password is
            </h1>
            <h2 style="font-family: 'futura', 'helvetica', sans-serif; color: #283845; font-size: 20px;">""" + content + """</h2>
            <br><br><br>

            You can login 
            <a href="partyfy.tfbr.me/login">Here</a> <br><br>
            <h1 style="font-family: 'futura', 'helvetica', sans-serif; color: white; font-size: 30px;">And have fun !</h1>
        </div>
        </body>
        </html>
        """
    text = content
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
        server.quit()

         


