import json
from os.path import exists
from os import makedirs
from src.ui import *

CONTACTS_DIR = "data/contacts/"
CONTACTS_PATH = "data/contacts/contacts.json"

def load_contacts():
    """
    Loads the contacts dictionary from the CONTACTS_PATH.

    Returns:
        A dictionary of contacts, in the format:
        { 
            "name": { 
                        "ip": <ip>,
                        "fingerprint": <fingerprint>,
                        "messages": {   "time": <time>,
                                        "to": <name>,
                                        "from": <name/ip>,
                                        "contents": <text> 
                                    }
                    }
        }
    """
    try:
        with open(CONTACTS_PATH, "r") as contacts_file:
            return json.load(contacts_file)
    except FileNotFoundError:
        return {}
    except OSError:
        if not exists(CONTACTS_DIR):
            makedirs(CONTACTS_DIR)
        else:
            print_red("Error: Contacts file not accessible.")
        return {}


def save_contacts(contacts):
    """
    Saves the contacts dictionary to the CONTACTS_PATH.

    Args:
        contacts: The contacts dictionary to save.
    """
    try:
        with open(CONTACTS_PATH, "w") as contacts_file:
            json.dump(contacts, contacts_file)
    except OSError:
        if not exists(CONTACTS_DIR):
            makedirs(CONTACTS_DIR)
            with open(CONTACTS_PATH, "w") as contacts_file:
                json.dump(contacts, contacts_file)
        else:
            print_red("Error: Contacts file not accessible.")


def display_contact(name, contacts):
    """
    Displays information about a given contact.

    Args:
        name: The name of the contact to display.
        contacts: The contacts dictionary to read from.
    """
    print_green(name)
    print("IP:", contacts[name]["ip"])
    print("Fingerprint:", contacts[name]["fingerprint"])
    print()


def display_convo(contact):
    print_bar("CONVERSATION")
    for message in contact["messages"]:
        print("{} {}: {}".format(message["time"], message["from"], message["contents"]))
    print()


def display_messages(contacts):
    for contact in contacts:
        if contacts[contact]["messages"]:
            message = contacts[contact]["messages"][-1]["contents"]
            trimmed_msg = message if len(message) < 20 else (message[:27] + "...")
            timestamp = contacts[contact]["messages"][-1]["time"]
            print("{:10s}  >  {:30s}  <  {}".format(contact, trimmed_msg, timestamp))
        else:
            print("{:10s}  >  {:^30s}  <".format(contact, "-- No messages --"))
    print()

