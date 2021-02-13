from login import AuthError
import pickle
import base64
from random import randint
from json import loads
from html2text import html2text
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from jinja2 import Template
from email.mime.text import MIMEText
from time import sleep

try:
    creds = pickle.load(open('token.pickle', 'rb')) # Authorize
except FileNotFoundError:
    raise(AuthError('token.pickle file not found. Run setup.sh to setup.'))

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
template_config = loads(open('config.json', 'r').read())
service = build('gmail', 'v1', credentials=creds) # Authorization
me_email = service.users().getProfile(userId='me').execute()['emailAddress']

def send_message(msg_txt, to, subject):
    message = MIMEText(msg_txt)
    message['to'] = to
    message['from'] = me_email
    message['subject'] = subject
    raw_msg = {'raw': (base64.urlsafe_b64encode(message.as_bytes()).decode())}
    service.users().messages().send(userId='me', body=raw_msg).execute()

class check(object):
    def __init__(self, message):
        self.message = message.lower()

    def check(self, keywords):
        # if a keyword is in the message, return True
        for keyword in keywords:
            if keyword in self.message:
                return(True)
        return(False)

    def problematic_assignment(self):
        keywords = [
            'missing', 
            'asap', 
            'due', 
            'responsible', 
            'last',
            'submit',
            'sumbission',
            'problem',
            'late',
            'was due',
            'partial'
        ]
        return(self.check(keywords))

    def absence(self):
        keywords = [
            'absent',
            'absence',
            'from class',
            'unexcused',
            'make up',
            'missed class',
            'not present',
            'attendance'
        ]
        return(self.check(keywords))

    def praise(self):
        # I myself have recieved much praise, so this list is quite long
        keywords = [
            'congratulate',
            'congratulations',
            'success',
            'honour',
            'participation',
            'perseverance',
            'growth mindset',
            'well done',
            'keep asking questions',
            'great job',
            'good job',
            'terrific',
            'positive',
            'A+',
            'role model',
            'well done',
            'just wanted to let you know',
            'thriving',
            'commend',
            'keep it up'
        ]
        return(self.check(keywords))

    def apology(self):
        keywords = [
            'apologize',
            'sorry',
            'regret',
            'forgive',
            'pardon',
            'inconvenience'
        ]
        return(self.check(keywords))

    def office_hours(self):
        keywords = [
            'office hours',
            'after school',
            'practice together',
            'extra help',
            'extra practice'
        ]
        return(self.check(keywords))

def main():
    messages = service.users().messages().list(userId='me').execute()['messages']
    first_message = messages[0] # Get ID of first message
    res = service.users().messages().get(userId='me', id=first_message['id']).execute() # Get data on the first message
    for i in res['payload']['headers']:
        if i['name'].lower() == 'from':
            raw_sender = i['value']
        if i['name'].lower() == 'subject':
            subject = i['value']
        if i['name'].lower() == 'return-path':
            sender_email = i['value'].replace('<', '').replace('>', '')

    if ',' in raw_sender:
        sender = raw_sender.replace('"', '') \
        [:raw_sender.index('<') - 3] \
        [:raw_sender.index(', ') - 1] # clean up gmail api's annoying stuff
    else:
        try:
            sender = raw_sender.replace('"', '') \
            [:raw_sender.index('<') - 1]
            sender = sender[sender.index(' ') + 1:]
        except:
            raise(ValueError('{} doesnt have a name'.format(raw_sender)))
    
    body = html2text(str(base64.urlsafe_b64decode(res['payload']['parts'][-1]['body']['data'])))

    if 'SENT' not in res['labelIds'] and sender_email not in config['ignore']: # if it's not sent by me and not in ignored adresses
        # check what kind of mail it is
        if check(body).problematic_assignment() == True: # if the assignemnt is problematic
            msg = Template(open('message_templates/problematic_assignment.jinja', 'r').read()).render(
                recipient=sender,
                farewell=template_config['farewell'],
                me=template_config['me']
            )
            send_message(msg, sender_email, subject)

        elif check(body).absence() == True:
            msg = Template(open('message_templates/absence.jinja', 'r').read()).render(
                recipient=sender,
                farewell=template_config['farewell'],
                me=template_config['me'],
                excuse=template_config['excuses'][randint(1, len(template_config['excuses']) - 1)] # get random excuse
            )
            send_message(msg, sender_email, subject)

        elif check(body).praise() == True:
            msg = Template(open('message_templates/praise.jinja', 'r').read()).render(
                recipient=sender,
                farewell=template_config['farewell'],
                me=template_config['me'],
            )
            send_message(msg, sender_email, subject)

        elif check(body).apology() == True:
            msg = Template(open('message_templates/praise.jinja', 'r').read()).render(
                recipient=sender,
                farewell=template_config['farewell'],
                me=template_config['me'],
            )
            send_message(msg, sender_email, subject)

        elif check(body).office_hours() == True:
            print(template_config['office_hours_time'])
            msg = Template(open('message_templates/office_hours.jinja', 'r').read()).render(
                recipient=sender,
                farewell=template_config['farewell'],
                me=template_config['me'],
                time=template_config['office_hours_time'] # get office hours time
            )
            send_message(msg, sender_email, subject)

if __name__ == '__main__':
    main()