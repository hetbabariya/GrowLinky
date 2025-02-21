import os
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from datetime import timedelta
import smtplib
from email.message import EmailMessage



load_dotenv()

def create_user_tokens(user_id):
    """Generate access and refresh tokens"""
    access_token_exp = int(os.getenv('ACCESS_TOKEN_EXPIRATION'))
    refresh_token_exp = int(os.getenv('REFRESH_TOKEN_EXPIRATION'))

    access_token = create_access_token(
        identity=user_id,
        expires_delta=timedelta(minutes=access_token_exp)
    )
    refresh_token = create_refresh_token(
        identity=user_id,
        expires_delta=timedelta(minutes=refresh_token_exp)
    )
    return access_token, refresh_token

def refresh_tokens(refresh_token):
    """Refresh the access token using the refresh token"""
    # If valid refresh token, create new access token

    access_token_exp = int(os.getenv('ACCESS_TOKEN_EXPIRATION'))

    return create_access_token(
        identity=get_jwt_identity(),
        expires_delta=timedelta(minutes=access_token_exp)
    )



def send_otp_email(to_email, otp):
    email_user = os.getenv("MAIL_USERNAME")
    email_password = os.getenv("MAIL_PASSWORD")

    if not email_user or not email_password:
        return {"error": "SMTP credentials are missing!"}

    subject = "Your OTP Code"
    body = f"Your Verification OTP is: {otp} \n\nThis OTP is valid for 2 minutes."

    try:
        message = EmailMessage()
        message.set_content(body)
        message["Subject"] = subject
        message["From"] = email_user
        message["To"] = to_email

        # Establish SMTP connection
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_user,email_password)
        server.send_message(message)
        server.quit()  #  Ensure connection is closed

        print(f" Email sent successfully to {to_email}")
        return {"message": "OTP email sent successfully"}

    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {str(e)}")
        return {"error": "SMTP Authentication failed. Check your EMAIL_USER and EMAIL_PASSWORD"}
    except smtplib.SMTPRecipientsRefused:
        return {"error": f"Recipient email address '{to_email}' is invalid"}
    except smtplib.SMTPException as e:
        return {"error": f"SMTP error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
