# Standard Library Imports
import json

# Flask Imports
from flask.views import MethodView
from flask import request, jsonify

# Project Imports
from interfaces import MemberInfo, BookInfo, BorrowBook, ReturnBook
from serializers import MembersEncoder
from response import SuccessResponse, ClientErrorResponse, ObjectCreatedResponse

class MembersAPI(MethodView):
    ''' API Service layer to handle incoming requests 
        to create, retreive, update or delete members
    '''    
    def get(self, member_id):
        if member_id is None:
            # Get all members
            # TODO: Implement pagination and limit
            member_info = MemberInfo().get_all_members()
        else:
            # Get single member
            member_info = MemberInfo().get_by_id(member_id)

        response = SuccessResponse(member_info)
        return response

    def post(self):
        # Create new member
        # Accepts data in json (POST body)
        data = request.get_json()
        email = data.get('email')
        if not email:
            # return client error
            return ClientErrorResponse(data='Email is required')
        username = data.get('username')
        if not username:
            # return client error
            return ClientErrorResponse(data='Username is required')
        created, message = MemberInfo().create_member(username, email)
        if created:
            # successfully created object
            response = ObjectCreatedResponse(message)
        else:
            # return client error
            response = ClientErrorResponse(message)
        return response

    def put(self, member_id):
        if not member_id:
            # return client error
            return ClientErrorResponse(data='Member ID is required')
        # accept data to be updated in json (post body)
        data = request.get_json()
        updated, message = MemberInfo().update_by_id(member_id, data)
        if updated:
            # success resposne
            response = SuccessResponse(message)
        else:
            # client error
            response = ClientErrorResponse(message)
        return response

    def delete(self, member_id):
        if not member_id:
            # client error
            return ClientErrorResponse(data='Member ID is required')
        deleted, message = MemberInfo().delete_by_id(member_id)
        if deleted:
            response = SuccessResponse(message)
        else:
            response = ClientErrorResponse(message)
        return response

class BooksAPI(MethodView):
    ''' API Service layer to handle incoming requests 
        to create, retreive, update or delete members
    '''    
    def get(self, book_id):
    
        if book_id is None:
            # Get all members
            # TODO: Implement pagination and limit
            books_info = BookInfo().get_all_books()
        else:
            # Get single members
            books_info = BookInfo().get_by_id(book_id)

        response = SuccessResponse(books_info)
        return response

    def post(self):
        # Adds new book
        # Accepts data in json (POST body)
        data = request.get_json()
        sku = data.get('sku')
        title = data.get('title')
        count = data.get('count')

        if not sku:
            return ClientErrorResponse(data='SKU is required')
        if not title:
            return ClientErrorResponse(data='title is required')
        if not count:
            return ClientErrorResponse(data='count is required')

        created, message = BookInfo().create_book(title, sku, count)
        if created:
            response = ObjectCreatedResponse(message)
        else:
            response = ClientErrorResponse(message)
        return response

    def put(self, book_id):
        if not book_id:
            return ClientErrorResponse(data='Book ID is required')
        # accept data to be updated in json (post body)
        data = request.get_json()
        updated, message = BookInfo().update_by_id(book_id, data)
        if updated:
            response = SuccessResponse(message)
        else:
            response = ClientErrorResponse(message)
        return response

    def delete(self, book_id):
        if not book_id:
            return ClientErrorResponse(data='Book ID is required')
        deleted, message = BookInfo().delete_by_id(book_id)
        if deleted:
            response = SuccessResponse(message)
        else:
            response = ClientErrorResponse(message)
        return response

class BorrowAPI(MethodView):

    def post(self):
        # Accepts book_id and member_id in json (post)
        # book id represents the book to be borrowed
        # member id represents the member to which book is rented
        data = request.get_json()
        book_id = data.get('book_id')
        member_id = data.get('member_id')
        if not book_id:
            return ClientErrorResponse(data='Book ID is required')
        if not member_id:
            return ClientErrorResponse(data='Member ID is required')
        rented, message = BorrowBook(book_id).rent_to_member(member_id)
        if rented:
            response = SuccessResponse(message)
        else:
            response = ClientErrorResponse(message)
        return response

class BookReturnAPI(MethodView):

    def post(self):
        # Accepts rented_id given as response in BorrowAPI 
        data = request.get_json()
        rented_id = data.get('rented_id')
        if not rented_id:
            return ClientErrorResponse(data='Rent ID is required')
        returned, message = ReturnBook(rented_id).returned_by_member()
        if returned:
            response = SuccessResponse(message)
        else:
            response = ClientErrorResponse(message)
        return response
