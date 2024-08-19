"""Example code for retrieving TPL checkout items and sending the parsed data
as a text message"""

from library import TPL
from lib_assets import Messenger

def tpl_with_google_doc_text_message(phone_number, username, password):
    tpl = TPL()
    messenger = Messenger(tpl.name)
    messenger.send_checkouts_text(phone_number, tpl.items_checked_out(username, password), "plain")

def tpl_without_text_message(phone_number, username, password):
    tpl = TPL()
    messenger = Messenger(tpl.name)
    messenger.send_checkouts_text(phone_number, tpl.items_checked_out(username, password), "doc")

if __name__ == "__main__":
    receiving_phone_number = "+1123456789"
    username = "my_username"
    password = "my_password"
    tpl_with_google_doc_text_message(receiving_phone_number, username, password)
    tpl_without_text_message(receiving_phone_number, username, password)