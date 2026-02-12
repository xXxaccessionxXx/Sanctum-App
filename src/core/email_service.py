import webbrowser
import smtplib
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    @staticmethod
    def send_via_client(subject, body, recipients=None):
        """
        Opens the default mail client with the email pre-filled.
        Safe, persistent, and requires no credentials.
        """
        if recipients is None:
            recipients = []
        
        # Join recipients with comma (or semicolon for some clients, but comma is standard)
        to_str = ",".join(recipients)
        
        # URL encode parameters
        subject_enc = urllib.parse.quote(subject)
        body_enc = urllib.parse.quote(body)
        
        mailto_url = f"mailto:{to_str}?subject={subject_enc}&body={body_enc}"
        webbrowser.open(mailto_url)

    @staticmethod
    def send_via_smtp(sender_email, sender_password, recipient_email, subject, body):
        """
        Sends an email using SMTP (e.g., Gmail).
        Tries TLS (587) first, then SSL (465).
        """
        errors = []
        
        # Method 1: TLS (Port 587)
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
            server.starttls()
            server.login(sender_email, sender_password)
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
            return True, "Email sent successfully via TLS."
        except Exception as e:
            errors.append(f"TLS(587) Error: {e}")

        # Method 2: SSL (Port 465) - Retry
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
            server.login(sender_email, sender_password)
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
            return True, "Email sent successfully via SSL."
        except Exception as e:
            errors.append(f"SSL(465) Error: {e}")

        return False, "; ".join(errors)
