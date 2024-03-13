# ADDING GOOGLE DRIVE SUPPORT

import io
import os
import csv
import PyPDF2

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from driveapi.service import get_credentials

credentials_info = get_credentials()
credentials = service_account.Credentials.from_service_account_info(credentials_info)
service = build('drive', 'v3', credentials=credentials)

logs_id = os.environ.get('LOGS_ID')

# Save Logs
def upload_chat_to_drive(chat_history, file_name):
    # Convert chat history to CSV
    csv_output = io.StringIO()
    writer = csv.writer(csv_output)
    writer.writerows(chat_history)
    csv_output.seek(0)

    # File metadata
    file_metadata = {
        'name': file_name,
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [logs_id]
    }

    # Upload file
    media = MediaIoBaseUpload(csv_output, mimetype='text/csv')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()


## Read PDF files
def download_file(file_id):
    service = build('drive', 'v3', credentials=credentials)
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh

# Function to process a PDF file
def process_pdf(file_stream):
    if isinstance(file_stream, dict): # Check if PDF was obtained using Drag and Drop or Drive link
        file_path = file_stream['name'] # Use 'path' for local testing and 'name' for Gradio
        pdf_reader = PyPDF2.PdfReader(file_path)
    else:
        pdf_reader = PyPDF2.PdfReader(file_stream)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def drive_content(shared_folder_id):
    # List files in the folder
    results = service.files().list(q=f"'{shared_folder_id}' in parents", fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])

    content = ''
    for item in items:
        print(f"Processing file: {item['name']}")
        file_stream = download_file(item['id'])
        content += str(process_pdf(file_stream))
        
    return content