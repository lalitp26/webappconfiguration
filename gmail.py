from __future__ import print_function
import httplib2
import os
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API'
LABEL_ID = ['INBOX','TRASH','DRAFT','SPAM','STARRED','UNREAD']


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_mail_info(message):
    """
        Function return mail info such as
        [mailId] [Date] [From] [To] [Subject]
    """

    # for m in message:
    #     print(m)
    # print(message['threadId'])
    response = {'thread_id':message['threadId']}
    for m in message['payload']['headers']:
        
        if m['name'] in 'Date':
            print(type(m['value']))
            response['Date'] = m['value']
            
        if m['name'] in 'From':
            response['From'] = m['value']
        
        if m['name'] in 'To':
            response['To'] = m['value']

        if m['name'] in 'Subject':
            response['Subject'] = m['value']

    return response
    # print(response)

def get_mail_details(mail_id, service):
    """
    Gets the email details

    Args: 
        mail_id : Unique mail id.
        service : service object.

    """
    message = service.users().messages().get(userId='me', id=mail_id).execute()
    print(message)

def get_mail_by_label(labels, service):
    """
        labels =['INBOX','TRASH','DRAFT','SPAM','STARRED','UNREAD']
    """
    message = service.users().messages().list(userId='me', labelIds= labels).execute()

def get_mail_by_query(query, service):
    
    """
        Query such as from:example@gmail.com
        Please refer Gmail Api documentaiton from more queries
    """

    message = service.users().messages().list(userId='me', q=query).execute()

def get_all_mails(service):
    
    """
        Return first 100 mails
    """

    message = service.users().messages().list(userId='me').execute()


def get_all_labels(service):
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    for label in labels:
        print(label['name'])
    
    


def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    # results = service.users().labels().list(userId='me').execute()
    # results = service.users().labels().get(userId='me', id="UNREAD").execute()
    # labels = results.get('labels', [])
    # print(results)
    
    # message = service.users().messages().list(userId='me', labelIds= ['UNREAD'], q='from:lalitp26@gmail.com').execute()

    # for m in message['messages']:
    #     print(m['id'])
    #     get_mail_details(m['id'], service)
    #     break
    # message = service.users().messages().list(userId='me').execute()
    # message = service.users().messages().get(userId='me', id='15f572663e19a3e3').execute()
    # get_mail_info(message)
    # print(message)
    # print(message['labelIds'])
    # print(type(message))
    # ms = json.dumps(message)
    # print(type(ms))
    # print(json.loads(ms))   
    # for mess in message:
    #     for m in message['messages']:
    #         print(m['id'])
        # for h in mess['payload']['headers']:
        #     name = h['name']
        #     frm = h['value']
        #     if name in 'From':
        #         print(frm)
        # if h['name'] is 'From':
        #     print(h['value']) 
    
    # for k, v in message.items():
    #     print(message['payload'])
    # for m in message['payload']:
    #     print(m[0])
    # for lb in message['labelIds']:
    #     if 'UNREAD' in lb:
    #         print(message)

    # if not labels:
    #     print('No labels found.')
    # else:
    #   print('Labels:')
    # for label in labels:
    #     print(label['name'])


if __name__ == '__main__':
    main()