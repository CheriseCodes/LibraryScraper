"""
Library containing classes that represent assets that libraries require for operation

Classes:
- Item: an item that can be checked out or put on hold in a library
- Messenger: used to formulate and send text messages on behalf of the library
"""
from datetime import date

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import os
from twilio.rest import Client


class Item:
    """
    A library item

    Attributes
    ----------
    data_received: datetime.date
        The date that the data for this library item was retrieved from the website
    title: str
    contributors: str
    item_format: str
    is_hold: bool
    item_date: str
    status: str
    branch: str
    system: str
    """

    def __init__(self, date_retrieved=None, title=None, item_format=None, is_hold=None, status=None, item_date=None,
                 branch=None, system=None, contributors=None):
        self.date_retrieved = date_retrieved  # the date the data was retrieved from the website
        self.title = title
        self.item_format = item_format
        self.is_hold = is_hold  # HOLD=0, CHECKOUT=1
        self.status = status  # the status of the item depending on _type
        self.item_date = item_date  # the pick up date or due date depending on _type
        self.branch = branch
        self.system = system
        if self.system == 'toronto':
            contrib_lst = contributors.rsplit(',', 1)
            if contrib_lst[-1] == ' author.':
                contributors = contrib_lst[0]
            self.contributors = 'by ' + contributors
        else:
            self.contributors = contributors

    def __eq__(self, __o: object) -> bool:
        return (__o.title == self.title) and (__o.item_format == self.item_format) and \
                    (__o.is_hold == self.is_hold) and (__o.status == self.status) and \
                           (__o.item_date == self.item_date) and (__o.branch == self.branch) and \
                           (__o.system == self.system) and (__o.contributors == self.contributors)

    def __str__(self):
        return f"Item(date_retrieved={self.date_retrieved},title={self.title},contributors={self.contributors}," \
               + f"item_format={self.item_format},is_hold={self.is_hold},status={self.status}," \
                f"item_date={self.item_date},branch={self.branch})"

    def generate_mock(self):
        """
        Formulates a string version of the command needed to create this object using the Item
        constructor.
        """
        new_mock = f"Item(date.today(),{self.title},{self.contributors},{self.item_format},{str(self.is_hold)},"
        + f"{self.item_date},{self.status},{self.branch},{self.system})"
        return new_mock


class Messenger:
    """
    Used to formulate and send text messages on behalf of the library
    """

    def __init__(self, region):
        self.region = region

    @staticmethod
    def text_string(lib_item):
        """
        Formulates a user-friendly text version of this item and returns the result as a string.
        Parameters
        ----------
        lib_item: Item
            The Item to represent as a string
        Returns
        -------
        str
        """
        if lib_item.title == '':
            return ''

        lib_item_status = ''
        if lib_item.status != '':
            lib_item_status = lib_item.status + " | "

        lib_item_branch = ''
        if lib_item.is_hold:
            lib_item_branch = ' | ' + lib_item.branch
        lib_item_title = ''
        if lib_item.title:
            lib_item_title = lib_item.title

        lib_item_format = ''
        if lib_item.item_format:
            lib_item_format = lib_item.item_format

        lib_item_date = ''
        if lib_item.item_date:
            lib_item_date = lib_item.item_date

        lib_item_contributors = ''
        if lib_item.contributors:
            lib_item_contributors = lib_item.contributors

        if lib_item.contributors == "":
            return lib_item_title + " (" + lib_item_format + ") | " + lib_item_status + lib_item_date + lib_item_branch
        else:
            return lib_item_title + " (" + lib_item_format + ") " + lib_item_contributors + ' | ' + lib_item_status \
                   + lib_item_date + lib_item_branch

    @staticmethod
    def formulate_text(checkouts, text_type):
        """
        Returns text that will be used as the body of a message that will be sent to the client

        Parameters
        ----------
        checkouts: Item[]
            A list of Items that contain data that will be listed in the text
        text_type: str
            The type of text message that should be sent ("doc", "plain")
        Returns
        -------
        str
        """
        res = ''
        # case 1: plain text
        if text_type == "plain":
            i = 1
            for item in checkouts:
                res += str(i) + '. ' + Messenger.text_string(item) + '\n'
                i += 1
        # case 2: Google doc link
        elif text_type == "doc":
            res += 'Click here to view your updated report: https://docs.google.com/document/d/' + \
                   os.environ['LIB_SCRAPER_DOC_ID']

        return res

    def formulate_checkouts_text(self, checkouts, text_type):
        """
        Returns the complete text that lists current checkouts

        Parameters
        ----------
        checkouts: Item[]
            A list of Items that contain data that will be listed in the text
        text_type: str
            The type of text message that should be sent ("doc", "plain")
        Returns
        -------
        str
        """
        res = '\n' + self.region + f" CHECKOUTS ({date.today()}):\n"
        res += self.formulate_text(checkouts, text_type)
        return res

    def formulate_holds_text(self, holds, text_type):
        """
        Returns the complete text that lists current holds

        Parameters
        ----------
        holds: Item[]
            A list of Items that contain data that will be listed in the text
        text_type: str
            The type of text message that should be sent ("doc", "plain")
        Returns
        -------
        str
        """
        res = '\n' + self.region + f" HOLDS ({date.today()}):\n"
        res += self.formulate_text(holds, text_type)
        return res

    def append_doc(self, items, is_hold):
        """
        Appends a report about items to the official Library Summary Google Doc

        Parameters
        ----------
        items: Item[]
            A list of Items that contain data that will be listed in the report
        is_hold: bool
            Indicates if the Items are hold items or checkout items
        """
        root_dir = os.path.dirname(os.path.abspath(__file__))
        scopes = ['https://www.googleapis.com/auth/documents']
        document_id = os.environ['LIB_SCRAPER_DOC_ID']
        # creds = Credentials.from_authorized_user_file('token.json', scopes)
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(root_dir, 'credentials.json'), scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('docs', 'v1', credentials=creds)

        # formulate new content

        if is_hold:
            new_text = self.formulate_holds_text(items, "plain")
        else:
            new_text = self.formulate_checkouts_text(items, "plain")

        new_text += '\n'

        req = [{
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': new_text
            }
        },
        ]
        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=document_id).execute()

        # print('The title of the document is: {}'.format(document.get('title')))

        service.documents().batchUpdate(documentId=document_id, body={'requests': req}).execute()

    def send_checkouts_text(self, phone_number, data, text_type):
        """
        Sends a text reporting the current status of checkouts at a Durham Library

        Parameters
        ----------
        data: Item[]
            A list of Items that contain data that will be listed in the text
        phone_number: the phone number that the text will be sent to. Must be in the
            format \+[0-9]* with the country calling code as a prefix.
        text_type: str
            The type of text message that should be sent ("doc", "plain")
        Returns
        -------
        TODO: What is the return type?
        """
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        res = self.formulate_checkouts_text(data, text_type)
        message = client.messages \
            .create(
            body=res,
            from_=os.environ['PHONE_FROM'],
            to=phone_number
        )
        return message

    def send_holds_text(self, phone_number, data, text_type):
        """
        Sends a text reporting the current status of holds at a Durham Library

        Parameters
        ----------
        data: Item[]
            A list of Items that contain data that will be listed in the text
        phone_number: the phone number that the text will be sent to. Must be in the
            format \+[0-9]* with the country calling code as a prefix.
        text_type: str
            The type of text message that should be sent ("doc", "plain")
        Returns
        -------
        An HTTP response attained after sending the text using the Twilio API
        """
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        res = self.formulate_holds_text(data, text_type)
        message = client.messages.create(
            body=res,
            from_=os.environ['PHONE_FROM'],
            to=phone_number
        )
        return message
