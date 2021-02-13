import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow

class AuthError(Exception):
    pass

if __name__ == '__main__':
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    if not os.path.exists('credentials.json'):
        raise(AuthError('No credentials file found. Visit https://github.com/gadhagod/automail for setup instructions,'))
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    pickle.dump(creds, open('token.pickle', 'wb'))

    print('Authorized')