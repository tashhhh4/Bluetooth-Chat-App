from db.engine import get_session
from models import Contact

def create_contact(name):
    """ Create a record of a human being known to the user. """
    session = get_session()
    try:
        contact = Contact(name=name)
        session.add(contact)
        session.commit()
        return contact
    finally:
        session.close()

def list_contacts():
    """ List Contacts tracked by the app. """
    session = get_session()
    try:
        return session.query(Contact).all()
    finally:
        session.close()

def get_contact(id):
    """ Retrieves a single Contact record by id. """
    session = get_session()
    try:
        return session.get(Contact, id)
    finally:
        session.close()

def update_contact(id, name):
    """ Update details of a Contact. """
    session = get_session()
    try:
        contact = session.get(Contact, id)
        contact.name = name
        session.update(contact)
        session.commit()
        return contact
    finally:
        session.close()

def delete_contact(id):
    """ Remove a Contact from the user's Blu2 Contact list. """
    session = get_session()
    try:
        contact = session.get(Contact, id)
        session.delete(contact)
        session.commit()
        return contact
    finally:
        session.close()