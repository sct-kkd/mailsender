import base64
import csv
import httplib2
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Gmail API setup steps:

# 1. Enable the Gmail API:
#   - Go to https://console.developers.google.com/apis/api/gmail.googleapis.com/
#   - Click "Enable"

# 2. Create OAuth credentials:
#   - Go to https://console.developers.google.com/apis/credentials
#   - Click "Create credentials" -> "OAuth client ID"
#   - Choose "Desktop app"
#   - Download the credentials.json file

# 3. Install the required libraries:
#   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Authentication flow
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes=['https://www.googleapis.com/auth/gmail.send'])
credentials = flow.run_local_server(port=0)

# Create Gmail API service
service = build('gmail', 'v1', credentials=credentials)

# Function to create a message with image
def create_message_with_image(to, subject, message_text, image_path):
    message = MIMEMultipart('related')
    message['to'] = to
    message['from'] = 'cabsinchandu@gmail.com'  # Replace with your actual Gmail address
    message['subject'] = subject

    msg_alternative = MIMEMultipart('alternative')
    message.attach(msg_alternative)

    msg_text = MIMEText(message_text, 'plain')
    msg_alternative.attach(msg_text)

    msg_html = MIMEText('<img src="cid:image1">', 'html')
    msg_alternative.attach(msg_html)

    fp = open(image_path, 'rb')
    msg_image = MIMEImage(fp.read())
    fp.close()

    msg_image.add_header('Content-ID', '<image1>')
    message.attach(msg_image)

    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    return {'raw': raw}

# Read recipient emails from CSV
with open('001.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        to = row[0]
        subject = 'Your email subject'
        message_text = 'Your email message text'
        image_path = '2.png'
        
        message = create_message_with_image(to, subject, message_text, image_path)
        print(to,message)
        try:
            service.users().messages().send(userId='me', body=message).execute()
            print(f'Email sent to {to}')
        except Exception as e:
            print(f'Error sending email to {to}: {e}')
