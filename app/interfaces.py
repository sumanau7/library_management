from data_access_layer import RetrieveMemberData, CreateMember, UpdateMember, DeleteMember
from data_access_layer import RetrieveBookData, CreateBook, UpdateBook, DeleteBook
from data_access_layer import UpdateBookAsRented, UpdateBookAsReturned, RetrieveRentData

class MemberInfo(object):
    """Interface for service layer, to access and process member info
        All business logic is consumed by this class
        where as appropiate classes are called to access data
    """
    def __init__(self):
        super(MemberInfo, self).__init__()
    
    def get_all_members(self):
        # calls data access layer class to retireve data from the repository
        member_data = RetrieveMemberData().get_all_members()
        return member_data

    def get_by_id(self, member_id):
        # Get Member info by ID
        member_data = RetrieveMemberData(member_id).get_members()
        return member_data

    def create_member(self, username, email):
    	# Call any Business logic here
    	# For example: save username to redis so as to provide username conflict
    	# response in UI layer etc.

    	# can be used as a pre hook logic and post hook logic
    	# Send the data to database for save.
    	member_created, message = CreateMember(username, email).save()
    	return member_created, message

    def update_by_id(self, member_id, data):
    	# Send the data to get update in database.
        member_updated, message = UpdateMember(member_id).save(data)
        return member_updated, message

    def delete_by_id(self, member_id):
    	# Send the data to get deleted from database.
		deleted, message = DeleteMember(member_id).delete()
		return deleted, message

class BookInfo(object):
    """Interface for service layer, to access and process books info
        All business logic is consumed by this class
        where as appropiate classes are called to access data
    """
    def __init__(self):
        super(BookInfo, self).__init__()
    
    def get_all_books(self):
        # calls the data access layer class to retireve data from the 
        # repository.
        book_data = RetrieveBookData().get_all_books()
        return book_data

    def get_by_id(self, book_id):
        # Get book info using ID
        book_data = RetrieveBookData(book_id).get_book()
        return book_data

    def create_book(self, sku, title, count):
    	# Call any Business logic here
    	# For example: save username to redis so as to provide username conflict
    	# response in UI layer etc.

    	# can be used as a pre hook logic and post hook logic
    	# Send the data to database for save.
    	book_created, message = CreateBook(sku, title, count).save()
    	return book_created, message

    def update_by_id(self, book_id, data):
    	# Send the data to get update in database.
        book_updated, message = UpdateBook(book_id).save(data)
        return book_updated, message

    def delete_by_id(self, book_id):
    	# Send the data to get deleted from database.
		deleted, message = DeleteBook(book_id).delete()
		return deleted, message

class RentInfo(object):
    """Interface for service layer, to access and process books info
        All business logic is consumed by this class
        where as appropiate classes are called to access data
    """
    def __init__(self):
        super(RentInfo, self).__init__()
    
    def get_by_id(self, rent_id):
        # Get rent details for the book given a rent id
        rent_data = RetrieveRentData(rent_id).get_rent_info()
        return rent_data

class BorrowBook(object):
    """ Implements the use case where member can borrow an available book
    """
    def __init__(self, book_id):
        self.book_id = book_id

    def rent_to_member(self, member_id):
        # Check if book is availabe by ID
        books_info = BookInfo().get_by_id(self.book_id)
        if not books_info:
            return False, 'Book Not Found'
        book_info = books_info[0]
        # As book is available in db, we have to make sure its
        # stock is available
        count_available = book_info.get('count', 0)
        if count_available == 0:
            return False, 'Book not in stock'
        # Verify the member before renting the book to member
        members_info = MemberInfo().get_by_id(member_id)
        if not members_info:
            return False, 'Member not found'
        member_info = members_info[0]
        rented, message = UpdateBookAsRented(self.book_id, count_available).rented_by_member(member_id)
        return rented, message

class ReturnBook(object):
    """ Returns the book borrowed by the member """
    def __init__(self, rented_id):
        self.rented_id = rented_id

    def returned_by_member(self):
        # Get rent details given a rent id
        rent_info = RentInfo().get_by_id(self.rented_id)
        if not rent_info:
            return False, 'No book rented using this ID'
        book_id = rent_info.get('book_id')
        member_id = rent_info.get('member_id')
        # retireive book details for the book ID
        books_info = BookInfo().get_by_id(book_id)
        book_info = books_info[0]
        count_available = book_info.get('count', 0)
        # update database records to mark the books as returned
        returned, message = UpdateBookAsReturned(self.rented_id,book_id, count_available).returned(member_id)
        return returned, message

