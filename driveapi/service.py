import os

def get_credentials():
# Authenticate with the service account
    client_email = os.environ.get('GOOGLE_CLIENT_EMAIL')
    private_key = os.environ.get('GOOGLE_PRIVATE_KEY').replace('\\n', '\n')
    token_uri = os.environ.get('GOOGLE_TOKEN_URI')


    # Create credentials object
    credentials_info = {
        'type': 'service_account',
        'client_email': str(client_email),
        'private_key': str(private_key),
        'token_uri': str(token_uri),
        'scopes': ['https://www.googleapis.com/auth/drive']
    }

    return credentials_info 


def get_shared_folder_id(drive_shared_link):
    
    start = drive_shared_link.find('/folders/') + 9
    end = drive_shared_link.find('?usp=sharing', start)
    shared_folder_id = str(drive_shared_link[start:end])
    
    return shared_folder_id
