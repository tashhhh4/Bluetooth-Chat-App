from db.engine import get_session
from models import Contact

def create_contact(name):
    """ Create a record of a human being known to the user. """
    with get_session() as session:
        contact = Contact(name=name)
        session.add(contact)
        session.commit()
        return contact

def list_contacts():
    """ List Contacts tracked by the app. """
    with get_session() as session:
        return session.query(Contact).all()

def get_contact(id):
    """ Retrieves a single Contact record by id. """
    with get_session() as session:
        return session.get(Contact, id)

def update_contact(id, name):
    """ Update details of a Contact. """
    with get_session() as session:
        contact = session.get(Contact, id)
        contact.name = name
        session.update(contact)
        session.commit()
        return contact

def delete_contact(id):
    """ Remove a Contact from the user's Blu2 Contact list. """
    with get_session() as session:
        contact = session.get(Contact, id)
        session.delete(contact)
        session.commit()
        return contact
