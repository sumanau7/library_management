# Generic Imports
import traceback
import logging

# App Imports
from app import db

# Exceptions Import
from sqlalchemy.exc import InterfaceError, IntegrityError

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr(self):
        return '<Member %r>' %(self.username)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(64), index=True, unique=True)
    title = db.Column(db.String(256))
    count = db.Column(db.Integer, nullable=False)


    def __repr(self):
        return '<Book %r>' %(self.title)

class BorrowList(db.Model):
    # Junction table defining many to many relation b/w
    # book rented and rented by member
    rented_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    borrowed_at = db.Column(db.DateTime, default=db.func.current_timestamp()) 
    returned_at = db.Column(db.DateTime)

    def __repr(self):
        return '<Book %r borrowed by %r' %(self.book_id.title, self.member_id.username)
    
