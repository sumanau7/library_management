# Generic Imports
import uuid
import traceback
import logging
import datetime

# App Imports
from app import db
from app.models import Member, Book, BorrowList

# Exceptions Import
from sqlalchemy.exc import InterfaceError, IntegrityError

class RetrieveMemberData(object):
    def __init__(self, member_id=None):
        self.member_id = member_id

    def get_members(self):
        # Get member by ID
        if not self.member_id:
            return []
        member = Member.query.get(self.member_id)
        member_data = {'id': member.id,
                       'username': member.username,
                       'email': member.email
                       }
        return [member_data]

    def get_all_members(self):
        # get all members
        members = Member.query.all()
        all_members = []
        for member in members:
            all_members.append({'id': member.id,
                       'username': member.username,
                       'email': member.email
                       })
        return all_members

class CreateMember(object):
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def save(self):
        try:
            # Create new member
            member = Member(username=self.username, email=self.email)
            db.session.add(member)
            db.session.commit()
            return True, 'created'

        except InterfaceError:
            logging.error("Got exception while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except IntegrityError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

class UpdateMember(object):
    def __init__(self, member_id):
        self.member_id = member_id
    
    def save(self, data):
        try:
            # updates member
            updated = db.session.query(Member).filter_by(id=self.member_id).update(data)
            db.session.commit()
            if updated:
                return True, 'updated'
            else:
                return False, 'Member ID not found'

        except InterfaceError:
            logging.error("Got exception while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except IntegrityError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

class DeleteMember(object):
    def __init__(self, member_id):
        self.member_id = member_id

    def delete(self):
        try:
            # delete member
            member = Member.query.get(self.member_id)
            if member:
                db.session.delete(member)
                db.session.commit()
                return True, 'deleted'
            else:
                return False, 'Member ID Not Found'

        except InterfaceError:
            logging.error("Got exception while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except IntegrityError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

class RetrieveBookData(object):
    def __init__(self, book_id=None):
        self.book_id = book_id

    def get_book(self):
        # Get book details
        if not self.book_id:
            return []
        book = Book.query.get(self.book_id)
        book_data = {'id': book.id,
                     'sku': book.sku,
                     'title': book.title,
                     'count': book.count
                       }
        return [book_data]

    def get_all_books(self):
        # get all book details
        books = Book.query.all()
        all_books = []
        for book in books:
            all_books.append({'id': book.id,
                       'sku': book.sku,
                       'title': book.title,
                       'count': book.count
                       })
        return all_books

class RetrieveRentData(object):
    def __init__(self, rent_id):
        self.rent_id = rent_id

    def get_rent_info(self):
        # retrieve details for the borrowed book
        rent = BorrowList.query.get(self.rent_id)
        rent_data = {'rented_id': rent.rented_id,
                     'book_id': rent.book_id,
                     'member_id': rent.member_id,
                     }
        return rent_data

class CreateBook(object):
    def __init__(self, sku, title, count):
        self.sku = sku
        self.title = title
        self.count = count

    def save(self):
        # adds a new book
        try:
            book = Book(sku=self.sku, title=self.title, count=self.count)
            db.session.add(book)
            db.session.commit()
            return True, 'created'

        except InterfaceError:
            logging.error("Got exception while creating new book: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except IntegrityError as e:
            logging.error("Got Integrity error while creating new book: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

class UpdateBook(object):
    def __init__(self, book_id):
        self.book_id = book_id
    
    def save(self, data):
        try:
            # updates the book for example: updates the stock for the book
            updated = db.session.query(Book).filter_by(id=self.book_id).update(data)
            db.session.commit()
            if updated:
                return True, 'updated'
            else:
                return False, 'Book ID not found'

        except InterfaceError:
            logging.error("Got exception while creating new book: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except IntegrityError as e:
            logging.error("Got Integrity error while creating new book: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

class DeleteBook(object):
    def __init__(self, book_id):
        self.book_id = book_id

    def delete(self):
        try:
            # deletes the book
            book = Book.query.get(self.book_id)
            if book:
                db.session.delete(book)
                db.session.commit()
                return True, 'deleted'
            else:
                return False, 'book ID Not Found'

        except InterfaceError:
            logging.error("Got exception while creating new book: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except IntegrityError as e:
            logging.error("Got Integrity error while creating new book: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

class UpdateBookAsRented(object):
    def __init__(self, book_id, count_available):
        self.book_id = book_id
        self.count_available = count_available

    def rented_by_member(self, member_id):
        try:
            self.member_id = member_id
            # Reduce the available count of the book
            data = {'count': self.count_available - 1}
            # update the book count
            UpdateBook(self.book_id).save(data)
            # Save borrowed entry to database
            borrowed = BorrowList(member_id=self.member_id, book_id=self.book_id)
            db.session.add(borrowed)
            db.session.commit()
            return True, 'rented'
        except InterfaceError:
            logging.error("Got exception while creating new book: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except IntegrityError as e:
            logging.error("Got Integrity error while creating new book: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

class UpdateBookAsReturned(object):
    def __init__(self, rented_id, book_id, count_available):
        self.rented_id = rented_id
        self.book_id = book_id
        self.count_available = count_available

    def returned(self, member_id):
        try:
            # Increase the available count of the book
            data = {'count': self.count_available + 1}
            # update the book count
            UpdateBook(self.book_id).save(data)
            # Save borrowed entry to database
            current_time = datetime.datetime.now()
            data = {'returned_at': current_time}
            returned = db.session.query(BorrowList).filter_by(
                                                rented_id=self.rented_id).update(data)

            db.session.commit()
            return True, 'returned'
        except InterfaceError:
            logging.error("Got exception while creating new book: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except IntegrityError as e:
            logging.error("Got Integrity error while creating new book: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()
