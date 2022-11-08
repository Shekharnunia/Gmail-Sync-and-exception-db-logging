from django.shortcuts import render
import os.path
from django.http import Http404
from django.core.exceptions import BadRequest
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from .models import Mail, ErrorLog
from .serializers import MailSerializer
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView

import base64
from email.message import EmailMessage
from email.mime.text import MIMEText

import google.auth

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
MAIL_SCOPES = 'https://mail.google.com/'


# Create your views here.
def messages_list_test(request):
    print(1)
    raise Http404
    # raise BadRequest
    # import djangos
    return render(request, "", {})


def create_message(sender, to, message_id, thread_id, subject, message_text):
    message = MIMEText(message_text)
    message['from'] = sender
    message['to'] = to
    message['In-Reply-To'] = message_id
    message['References'] = message_id
    message['subject'] = subject

    return {
        'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode(),
        'threadId':thread_id
    }


class GmailAuthMixin:

    def auth(self, auth_type=None):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        module_dir = os.path.dirname(__file__)
        token_file_path = os.path.join(module_dir, 'token.json')
        credentials_file_path = os.path.join(module_dir, 'credentials.json')
        
        # print(os.path.exists(token_file_path))
        scope = SCOPES
        if auth_type == "support":
            scope = MAIL_SCOPES
        print(scope)
        if os.path.exists(token_file_path):
            creds = Credentials.from_authorized_user_file(token_file_path, scope)
        # print(creds)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file_path, scope)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file_path, 'w') as token:
                token.write(creds.to_json())
        return creds
        

class SyncMail(GmailAuthMixin, APIView):

    def get(self, request, format=None):
        creds = self.auth()
        try:
            # Call the Gmail API
            service = build('gmail', 'v1', credentials=creds)
            results = service.users().messages().list(userId='me').execute()
            messages = results.get('messages', [])
            # messages.reverse()

            if not messages:
                return
            messages_body = []

            # get last message id
            message = Mail.objects.order_by("id").last()
            message_id = message.message_id if message else None
            if not message_id:
                messages.reverse()
            for message in messages:
                if message_id != str(message["id"]):
                    message_body = service.users().messages().get(userId='me', id=message["id"], format="minimal").execute()
                    messages_body.append(message_body)
                    Mail.objects.update_or_create(message_id=message["id"], thread_id=message["threadId"], snippet=message_body["snippet"])
                else:
                    break
        except HttpError as error:
        #     # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')
        return Response(messages_body)


class SupportMail(GmailAuthMixin, APIView):

    def get(self, request, format=None):
        creds = self.auth(auth_type="support")
        try:
            # Call the Gmail API
            service = build('gmail', 'v1', credentials=creds)
            results = service.users().messages().list(userId='me', q="Please Help Me!").execute()
            messages = results.get('messages', [])
            # print(messages)

            message = create_message('shekharnuniagaming2@gmail.com','shekharnunia@gmail.com', 
    messages[0]["id"], messages[0]["threadId"], "Hi", "Hello There, We will get back to you on this.")
            message = (service.users().messages().send(userId="me", body=message).execute())
            print(messages)
        except HttpError as error:
        #     # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')
        return Response(messages)



class MailList(generics.ListAPIView):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer
    
    
    # def list(self, request, format=None):
        
    #     return Response({})
        

def messages_list(request):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    module_dir = os.path.dirname(__file__)
    token_file_path = os.path.join(module_dir, 'token.json')
    credentials_file_path = os.path.join(module_dir, 'credentials.json')
    
    if os.path.exists(token_file_path):
        creds = Credentials.from_authorized_user_file(token_file_path, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file_path, 'w') as token:
            token.write(creds.to_json())
    context = {}
    return render(request, "message-list.html", context)


class ErrorLogList(ListView):
    template_name = "errorlog_list.html"
    # specify the model for list view
    model = ErrorLog


class ErrorLogDetail(DetailView):
    template_name = "errorlog.html"
    # specify the model for list view
    model = ErrorLog


class ErrorLogDelete(DeleteView):
    template_name = "errorlog.html"
    # specify the model for list view
    model = ErrorLog
    success_url = "/errors/"